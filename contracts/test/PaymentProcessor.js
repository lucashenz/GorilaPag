const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PaymentProcessor", function () {
  let PaymentProcessor, paymentProcessor;
  let owner, merchant, user;

  beforeEach(async function () {
    [owner, merchant, user] = await ethers.getSigners();

    const platformWallet = owner.address;
    const feePercent = 100; // 1% (100 basis points)

    PaymentProcessor = await ethers.getContractFactory("PaymentProcessor");
    paymentProcessor = await PaymentProcessor.deploy(platformWallet, feePercent);
    await paymentProcessor.waitForDeployment();
  });

  it("deve permitir que o usuário envie um pagamento", async function () {
    const paymentId = 1;
    const paymentAmount = ethers.parseEther("1");

    await paymentProcessor.connect(merchant).createPayment(paymentId, paymentAmount);

    const tx = await paymentProcessor.connect(user).pay(paymentId, { value: paymentAmount });
    await tx.wait();

    const payment = await paymentProcessor.payments(paymentId);
    expect(payment.paid).to.equal(true);
    expect(payment.amount).to.equal(paymentAmount);
  });

  it("deve comparar gas entre pay (external) e payP (public)", async function () {
    const paymentId = 2;
    const paymentAmount = ethers.parseEther("1");

    await paymentProcessor.connect(merchant).createPayment(paymentId, paymentAmount);
    const txExternal = await paymentProcessor.connect(user).pay(paymentId, { value: paymentAmount });
    const receiptExternal = await txExternal.wait();

    const paymentId2 = 3;
    await paymentProcessor.connect(merchant).createPayment(paymentId2, paymentAmount);
    const txPublic = await paymentProcessor.connect(user).payP(paymentId2, { value: paymentAmount });
    const receiptPublic = await txPublic.wait();

    // Converter BigInt para Number
    const gasExternal = Number(receiptExternal.gasUsed);
    const gasPublic = Number(receiptPublic.gasUsed);
    const saving = (((gasExternal - gasPublic) / gasExternal) * 100).toFixed(2);

    console.table({
      "pay (external)": gasExternal,
      "payP (public)": gasPublic,
      "saving (%)": saving,
    });

    expect(gasExternal).to.be.greaterThan(gasPublic);
  });
});
