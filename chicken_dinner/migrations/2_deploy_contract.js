var contract = artifacts.require("EthExchange");

module.exports = function(deployer) {
    deployer.deploy(contract);
};
