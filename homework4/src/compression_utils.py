import copy
from queue import *
from dataclasses import *
from typing import *
from byte_utils import *

# [!] Important: This is the character code of the End Transmission Block (ETB)
# Character -- use this constant to signal the end of a message
ETB_CHAR = "\x17"


class HuffmanNode:
    '''
    HuffmanNode class to be used in construction of the Huffman Trie
    employed by the ReusableHuffman encoder/decoder below.
    '''

    # Educational Note: traditional constructor rather than dataclass because of need
    # to set default values for children parameters
    def __init__(self, char: str, freq: int,
                 zero_child: Optional["HuffmanNode"] = None,
                 one_child: Optional["HuffmanNode"] = None):
        '''
        HuffNodes represent nodes in the HuffmanTrie used to create a lossless
        encoding map used for compression. Their properties are given in this
        constructor's arguments:
        
        Parameters:
            char (str):
                Really, a single character, storing the character represented
                by a leaf node in the trie
            freq (int):
                The frequency with which the character / characters in a subtree
                appear in the corpus
            zero_child, one_child (Optional[HuffmanNode]):
                The children of any non-leaf, or None if a leaf; the zero_child
                will always pertain to the 0 bit part of the prefix, and vice
                versa for the one_child (which will add a 1 bit to the prefix)
        '''
        self.char = char
        self.freq = freq
        self.zero_child = zero_child
        self.one_child = one_child

    def is_leaf(self) -> bool:
        '''
        Returns:
            bool:
                Whether or not the current node is a leaf
        '''
        return self.zero_child is None and self.one_child is None


class ReusableHuffman:
    '''
    ReusableHuffman encoder / decoder that is trained on some original
    corpus of text and can then be used to compress / decompress other
    text messages that have similar distributions of characters.
    '''

    def __recurse(self, node: HuffmanNode, bitstring: str, bitstring_storage: dict[HuffmanNode, str]) -> None:
        '''
        Recursive method that traverses through the huffman trie top-down to
        add the bitcodes to each letter found within the original corpus.

        Parameters:
            node (HuffmanNode):
                The current node within the huffman trie represented with
                either a "0" or "1"  bit.
            bitstring (str):
                The current bitstring associated with the current node.
            bitstring_storage (dict[HuffmanNode, str]):
                The storage dictionary for holding the bitstring code associated with each character.
        '''
        if node.is_leaf():
            self._encoding_map[node.char] = bitstring_storage[node]
        if node.zero_child is not None:
            bitstring += "0"
            bitstring_storage[node.zero_child] = bitstring
            self.__recurse(node.zero_child, bitstring, bitstring_storage)
            bitstring = bitstring[:-1]
        if node.one_child is not None:
            bitstring += "1"
            bitstring_storage[node.one_child] = bitstring
            self.__recurse(node.one_child, bitstring, bitstring_storage)

    def __init__(self, corpus: str):
        '''
        Constructor for a new ReusableHuffman encoder / decoder that is fit to
        the given text corpus and can then be used to compress and decompress
        messages with a similar distribution of characters.

        Parameters:
            corpus (str):
                The text corpus on which to fit the ReusableHuffman instance,
                which will be used to construct the encoding map
        '''
        self._encoding_map: dict[str, str] = dict()

        node_queue: PriorityQueue[tuple[tuple[int, str], HuffmanNode]] = PriorityQueue()
        letter_frequency: dict[str, int] = dict()

        if len(corpus) == 0:
            self._encoding_map[ETB_CHAR] = "0"
        else:
            corpus += ETB_CHAR
            # >> [BAC] Finding the character distribution should be a helper method. (-0.5)
            for letter in corpus:
                if letter not in letter_frequency:
                    letter_frequency[letter] = 1
                else:
                    letter_frequency[letter] += 1

            for letter, frequency in letter_frequency.items():
                new_node: HuffmanNode = HuffmanNode(letter, frequency)
                node_queue.put(((new_node.freq, new_node.char), new_node))
            # >> [BAC] Building the Huffman Trie should be a helper method. (-0.5)
            while node_queue.qsize() > 1:
                zero_child: HuffmanNode = node_queue.get()[1]
                one_child: HuffmanNode = node_queue.get()[1]
                parent_node: HuffmanNode = HuffmanNode("", zero_child.freq + one_child.freq, zero_child, one_child)
                if ord(zero_child.char) < ord(one_child.char):
                    parent_node.char = zero_child.char
                else:
                    parent_node.char = one_child.char
                node_queue.put(((parent_node.freq, parent_node.char), parent_node))

            self._trie_root: HuffmanNode = node_queue.get()[1]
            bitstring_storage: dict[HuffmanNode, str] = dict()
            starting_bitstring: str = ""
            self.__recurse(self._trie_root, starting_bitstring, bitstring_storage)

    def get_encoding_map(self) -> dict[str, str]:
        '''
        Simple getter for the encoding map that, after the constructor is run,
        will be a dictionary of character keys mapping to their compressed
        bitstrings in this ReusableHuffman instance's encoding
        
        Example:
            {ETB_CHAR: 10, "A": 11, "B": 0}
            (see unit tests for more examples)
        
        Returns:
            dict[str, str]:
                A copy of this ReusableHuffman instance's encoding map
        '''
        return copy.deepcopy(self._encoding_map)

    # Compression
    # ---------------------------------------------------------------------------

    def compress_message(self, message: str) -> bytes:
        '''
        Compresses the given String message / text corpus into its Huffman-coded
        bitstring, and then converted into a Python bytes type.
        
        [!] Uses the _encoding_map attribute generated during construction.
        
        Parameters:
            message (str):
                String representing the corpus to compress
        
        Returns:
            bytes:
                Bytes storing the compressed corpus with the Huffman coded
                bytecode. Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            compressed_message = huff_coder.compress_message("ABBBCC")
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            solution = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual(solution, compressed_message)
        '''

        bitstring_header: str = ""
        for letter in message:
            bitstring_header += self._encoding_map[letter]

        bitstring_header += self._encoding_map[ETB_CHAR]

        bitstrings: list[str] = []
        while len(bitstring_header) > 8:
            bitstrings.append(bitstring_header[:8])
            bitstring_header = bitstring_header[8:]

        if len(bitstring_header) > 0:
            header_length: int = len(bitstring_header)
            bitstrings.append(bitstring_header + "0" * (8 - header_length))

        return bitstrings_to_bytes(bitstrings)

    # Decompression
    # ---------------------------------------------------------------------------

    def decompress(self, compressed_msg: bytes) -> str:
        '''
        Decompresses the given bytes representing a compressed corpus into their
        original character format.
        
        [!] Should use the Huffman Trie generated during construction.
        
        Parameters:
            compressed_msg (bytes):
                Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Returns:
            str:
                The decompressed message as a string.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            compressed_msg: bytes = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual("ABBBCC", huff_coder.decompress(compressed_msg))
        '''

        bits: str = ""
        for byte in compressed_msg:
            bits += byte_to_bitstring(byte)

        decoded_message: str = ""
        while len(bits) > 0:
            etb_char_length: int = len(self._encoding_map[ETB_CHAR])
            if self._encoding_map[ETB_CHAR] == bits[:etb_char_length]:
                return decoded_message
            for letter, bitcode in sorted(self._encoding_map.items(), key=lambda item: len(item[1]), reverse=True):
                for num in range(len(bitcode)):
                    if bits[num] == bitcode[num]:
                        if num == len(bitcode) - 1:
                            decoded_message += letter
                            bits = bits[num + 1:]
                        continue
                    else:
                        break
        return ""
# ===================================================
# >>> [BAC] Summary
# Excellent submission that has a ton to like and was
# obviously well-tested. Good delegation of labor into
# helper methods, generally clean style, and shows
# strong command of programming foundations alongside
# data structure and algorithmic concepts. Keep up
# the great work! 
# ---------------------------------------------------
# >>> [BAC] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
# 
# [X] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [X] Proper JavaDocs provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:       100.0 / 100 (-1.5 / missed test)
# Style Penalty:      -1
# Total:             99.0 / 100
# ===================================================
