// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EthExchange {
    mapping(address => uint256) public balance;

	event Deposited(address indexed sender, uint256 amount, uint256 balance_after);
	event Exchanged(address indexed sender, address indexed receiver, uint256 amount);

	function Deposit(address account, uint256 amount) external payable{
		require(amount > 0, "Must deposit more than 0 ETH");
		require(account != address(0), "Invalid address");
		balance[account] += amount;

		emit Deposited(account, amount, balance[account]);
	}

	function ExchangeETH(address sender, address receiver, uint256 amount) external payable{
		require(amount > 0, "Must exchange with more than 0ETH");
		require(sender != address(0) && receiver != address(0), "Invalid address");
		require(amount <= balance[sender], "Insufficient balance");


		emit Exchanged(sender, receiver, amount);

	}
}
