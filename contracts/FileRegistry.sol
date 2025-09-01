// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FileHash {
    struct FileMetaData {
        bytes32 fileHash;
        bytes32 merkleRootHash;
        address uploader;
        uint256 timestamp;
    }
    mapping(bytes32 => FileMetaData) public fileRegistry;
    event FileRegistered(
        bytes32 indexed fileHash,
        address indexed uploader,
        uint256 timestamp
    );
    function registerFile(bytes32 _fileHash, bytes32 _merkleRootHash) external {
        require(
            fileRegistry[_fileHash].fileHash == bytes32(0),
            "File already exists in the blockchain"
        );
        fileRegistry[_fileHash] = FileMetaData({
            fileHash: _fileHash,
            merkleRootHash: _merkleRootHash,
            uploader: msg.sender,
            timestamp: block.timestamp
        });
        emit FileRegistered(_fileHash, msg.sender, block.timestamp);
    }
    function getFileMetaData(
        bytes32 _fileHash
    ) external view returns (FileMetaData memory) {
        require(
            fileRegistry[_fileHash].fileHash != bytes32(0),
            "File with the given hash was not found"
        );
        return fileRegistry[_fileHash];
    }
}
