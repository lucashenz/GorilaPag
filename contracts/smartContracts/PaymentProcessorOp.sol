// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title PaymentProcessor - Simple and secure crypto payment contract
contract PaymentProcessor {
    address public platformWallet;  // wallet that receives the fee
    uint256 public feePercent;      // fee in basis points (100 = 1%)

    error customError();

    struct Payment {
        uint256 id;
        address merchant;
        uint256 amount;
        bool paid;
    }

    mapping(uint256 => Payment) public payments;

    event PaymentCreated(uint256 indexed id, address indexed merchant, uint256 amount);
    event PaymentCompleted(uint256 indexed id, address indexed payer, uint256 amount, uint256 fee);
    event FeeUpdated(uint256 oldFee, uint256 newFee);
    event PlatformWalletUpdated(address oldWallet, address newWallet);

    modifier onlyPlatform() {
        require(msg.sender == platformWallet, customError());
        _;
    }

    constructor(address _platformWallet, uint256 _feePercent) {
        require(_platformWallet != address(0), customError());
        require(_feePercent <= 1000, customError()); // max 10%
        platformWallet = _platformWallet;
        feePercent = _feePercent;
    }

    /// @notice Create a new payment request
    function createPayment(uint256 _id, uint256 _amount) external {
        require(_id != 0, customError());
        require(_amount > 0, customError());
        require(payments[_id].id == 0, customError());

        payments[_id] = Payment({
            id: _id,
            merchant: msg.sender,
            amount: _amount,
            paid: false
        });

        emit PaymentCreated(_id, msg.sender, _amount);
    }

    /// @notice Pay an existing payment request
    function pay(uint256 _id) external payable {
        Payment storage p = payments[_id];
        require(p.id != 0, customError());
        require(!p.paid, customError());
        require(msg.value == p.amount, customError());

        uint256 fee = (msg.value * feePercent) / 10000;
        uint256 merchantAmount = msg.value - fee;

        // send fee and payment
        (bool feeSent, ) = payable(platformWallet).call{value: fee}("");
        require(feeSent, customError());

        (bool paidMerchant, ) = payable(p.merchant).call{value: merchantAmount}("");
        require(paidMerchant, customError());

        p.paid = true;
        emit PaymentCompleted(_id, msg.sender, msg.value, fee);
    }

     /// @notice Pay an existing payment request
    function payP(uint256 _id) public payable {
        Payment storage p = payments[_id];
        require(p.id != 0, customError());
        require(!p.paid, customError());
        require(msg.value == p.amount, customError());

        uint256 fee = (msg.value * feePercent) / 10000;
        uint256 merchantAmount = msg.value - fee;

        // send fee and payment
        (bool feeSent, ) = payable(platformWallet).call{value: fee}("");
        require(feeSent, customError());

        (bool paidMerchant, ) = payable(p.merchant).call{value: merchantAmount}("");
        require(paidMerchant, customError());

        p.paid = true;
        emit PaymentCompleted(_id, msg.sender, msg.value, fee);
    }

    /// @notice Update the platform fee
    function updateFee(uint256 _newFee) external onlyPlatform {
        require(_newFee <= 1000, customError()); // max 10%
        emit FeeUpdated(feePercent, _newFee);
        feePercent = _newFee;
    }

    /// @notice Change the platform wallet
    function updatePlatformWallet(address _newWallet) external onlyPlatform {
        require(_newWallet != address(0), customError());
        emit PlatformWalletUpdated(platformWallet, _newWallet);
        platformWallet = _newWallet;
    }

    /// @notice Emergency withdraw if funds get stuck
    function emergencyWithdraw() external onlyPlatform {
        uint256 balance = address(this).balance;
        require(balance > 0, customError());
        payable(platformWallet).transfer(balance);
    }
}
