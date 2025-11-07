const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PaymentProcessor", function () {
  let paymentProcessor;
  let owner;
  let user;

  beforeEach(async function () {
    [owner, user] = await ethers.getSigners();

    const PaymentProcessor = await ethers.getContractFactory("PaymentProcessor");
    paymentProcessor = await PaymentProcessor.deploy();
    await paymentProcessor.waitForDeployment(); // compatível com Hardhat v2.22+
  });

  it("deve permitir que o usuário envie um pagamento", async function () {
    const paymentAmount = ethers.parseEther("1.0");

    // Envia pagamento
    await expect(
      user.sendTransaction({
        to: paymentProcessor.target, // target = endereço do contrato
        value: paymentAmount,
      })
    ).to.changeEtherBalances(
      [user, paymentProcessor],
      [paymentAmount * -1n, paymentAmount]
    );
  });

  it("deve permitir que o dono retire fundos", async function () {
    const paymentAmount = ethers.parseEther("1.0");

    // Usuário envia pagamento
    await user.sendTransaction({
      to: paymentProcessor.target,
      value: paymentAmount,
    });

    // Dono retira fundos
    await expect(paymentProcessor.connect(owner).withdraw()).to.changeEtherBalances(
      [paymentProcessor, owner],
      [-paymentAmount, paymentAmount]
    );
  });

  it("deve falhar se não for o dono tentando retirar", async function () {
    await expect(paymentProcessor.connect(user).withdraw()).to.be.revertedWith(
      "Only owner can withdraw"
    );
  });
});
