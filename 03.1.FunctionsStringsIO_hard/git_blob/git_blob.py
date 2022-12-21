import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class BlobType(Enum):
    """Helper class for holding blob type"""
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    """Any blob holder"""
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    """Commit blob holder"""
    tree_hash: str
    parents: list[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    """Tree blob holder"""
    children: dict[str, Blob]


def read_blob(path: Path) -> Blob:
    """
    Read blob-file, decompress and parse header
    :param path: path to blob-file
    :return: blob-file type and content
    """
    with open(path, 'rb') as file:
        rt = file.read()
        decompressed_text = zlib.decompress(rt)
        data = decompressed_text.split(b'\x00')
        type_ = data[0].split(b" ")[0]
        content = decompressed_text[len(data[0]) + 1:]
        return Blob(BlobType.from_bytes(type_), content=content)


def traverse_objects(obj_dir: Path) -> dict[str, Blob]:
    """
    Traverse directory with git objects and load them
    :param obj_dir: path to git "objects" directory
    :return: mapping from hash to blob with every blob found
    """
    p = Path(obj_dir)
    list_of_directories = [x for x in p.iterdir() if x.is_dir()]
    dict_str_to_blob: dict[str, Blob] = {}
    # print(list_of_directories)
    for directory in list_of_directories:
        list_of_files = list(directory.glob('*'))
        for file in list_of_files:
            file_parts = file.parts
            dict_str_to_blob[file_parts[-2] + file_parts[-1]] = read_blob(file)
    return dict_str_to_blob


def parse_commit(blob: Blob) -> Commit:
    """
    Parse commit blob
    :param blob: blob with commit type
    :return: parsed commit
    """
    content = blob.content
    data = content.split(b"\n")
    # print(data)
    commit_hash = data[0].split(b' ')[1]
    commit_parent = []
    commit_commiter = ""
    commit_author = ""
    # commit_message = ""
    index_of_message = 0
    for index, line in enumerate(data):
        if line == b'':
            index_of_message = index
            break
    commit_message = data[index_of_message + 1]
    for line in data:
        index = line.find(b' ')
        name = line[:index]
        content_of_name = line[index + 1:].decode()
        # print(name, content_of_name)
        # content_of_name = content_of_name.decode()
        if name == b'parent':
            commit_parent.append(content_of_name)
        if name == b'author':
            commit_author = content_of_name
        if name == b'committer':
            commit_commiter = content_of_name
    return Commit(tree_hash=commit_hash.decode(), parents=commit_parent, author=commit_author,
                  committer=commit_commiter, message=commit_message.decode())


def parse_tree(blobs: dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    """
    Parse tree blob
    :param blobs: all read blobs (by traverse_objects)
    :param tree_root: tree blob to parse
    :param ignore_missing: ignore blobs which were not found in objects directory
    :return: tree contains children blobs (or only part of them found in objects directory)
    NB. Children blobs are not being parsed according to type.
        Also nested tree blobs are not being traversed.
    """
    content = tree_root.content
    # print(content)
    # print(content.hex())
    # list_of_lines = content.split(b"\0")
    # print(list_of_lines[1][:20])
    list_of_names = []
    list_of_hash = []
    current_str = content
    dict_str_to_blob: dict[str, Blob] = {}
    while len(current_str) != 0:
        index = current_str.find(b"\0")
        # print(index)
        name = current_str[:index]
        hash = current_str[index + 1: index + 21]
        list_of_names.append(name)
        list_of_hash.append(hash.hex())
        # print(index + 21, len(current_str))
        current_str = current_str[index + 21:]
        # print(hash, hash.hex())
        # print(current_str)
        name = name.split(b' ')[1]
        try:
            dict_str_to_blob[name.decode()] = blobs[hash.hex()]
        except KeyError:
            pass
    return Tree(dict_str_to_blob)
    # print(list_of_names)
    # print(list_of_lines)
    # print(blobs.keys())


def find_initial_commit(blobs: dict[str, Blob]) -> Commit:
    """
    Iterate over blobs and find initial commit (without parents)
    :param blobs: blobs read from objects dir
    :return: initial commit
    """
    for key, blob in blobs.items():
        if blob.type_ != BlobType.COMMIT:
            continue
        # try:
        commit = parse_commit(blob)
        if commit.parents == []:
            return commit
        # except AttributeError:
            # pass
    return Commit("", [""], "", "", "")


def search_file(blobs: dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    """
    Traverse tree blob (can have nested tree blobs) and find requested file,
    check if file was not found (assertion).
    :param blobs: blobs read from objects dir
    :param tree_root: root blob for traversal
    :param filename: requested file
    :return: requested file blob
    """
    tree = parse_tree(blobs, tree_root)
    if filename in tree.children:
        return tree.children[filename]
    for name, blob in tree.children.items():
        if blob.type_ == BlobType.TREE:
            tr = search_file(blobs, blob, filename)
            if tr.content != b"":
                return tr
    return Blob(BlobType.TREE, b"")
