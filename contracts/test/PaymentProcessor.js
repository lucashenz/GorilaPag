const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("💰 Gas Efficiency Comparison - PaymentProcessor vs PaymentProcessorOP", function () {
  let owner, merchant, user;
  let ProcessorString, ProcessorError;
  let contractString, contractError;

  beforeEach(async function () {
    [owner, merchant, user] = await ethers.getSigners();

    const platformWallet = owner.address;
    const feePercent = 100; // 1%

    // Deploy versão com strings
    ProcessorString = await ethers.getContractFactory("PaymentProcessor");
    contractString = await ProcessorString.deploy(platformWallet, feePercent);
    await contractString.waitForDeployment();

    // Deploy versão com customError
    ProcessorError = await ethers.getContractFactory("PaymentProcessorOP");
    contractError = await ProcessorError.deploy(platformWallet, feePercent);
    await contractError.waitForDeployment();
  });

  async function simulatePayment(contract, label) {
    const paymentId = Math.floor(Math.random() * 10000);
    const paymentAmount = ethers.parseEther("1");

    // criar e pagar
    await contract.connect(merchant).createPayment(paymentId, paymentAmount);

    const tx = await contract.connect(user).pay(paymentId, { value: paymentAmount });
    const receipt = await tx.wait();

    return {
      label,
      gasUsed: Number(receipt.gasUsed),
    };
  }

  async function simulatePayP(contract, label) {
    const paymentId = Math.floor(Math.random() * 10000) + 5000;
    const paymentAmount = ethers.parseEther("1");

    await contract.connect(merchant).createPayment(paymentId, paymentAmount);

    const tx = await contract.connect(user).payP(paymentId, { value: paymentAmount });
    const receipt = await tx.wait();

    return {
      label,
      gasUsed: Number(receipt.gasUsed),
    };
  }

  it("🔥 compara consumo de gas entre strings e customError", async function () {
    const result1 = await simulatePayment(contractString, "String Errors (pay)");
    const result2 = await simulatePayment(contractError, "Custom Errors (pay)");

    const result3 = await simulatePayP(contractString, "String Errors (payP)");
    const result4 = await simulatePayP(contractError, "Custom Errors (payP)");

    console.table([
      result1,
      result2,
      result3,
      result4,
      {
        label: "Economia (pay)",
        gasUsed: `${(((result1.gasUsed - result2.gasUsed) / result1.gasUsed) * 100).toFixed(2)}%`,
      },
      {
        label: "Economia (payP)",
        gasUsed: `${(((result3.gasUsed - result4.gasUsed) / result3.gasUsed) * 100).toFixed(2)}%`,
      },
    ]);

    // simples validação só pra garantir que tudo rodou
    expect(result1.gasUsed).to.be.greaterThan(0);
    expect(result2.gasUsed).to.be.greaterThan(0);
  });
});
