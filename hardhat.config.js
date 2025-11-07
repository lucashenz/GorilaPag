require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  paths: {
    sources: "./contracts/smartContracts", // path smart contracts
    tests: "./contracts/test",             // path tests
    cache: "./cache",
    artifacts: "./artifacts"
  },
};
