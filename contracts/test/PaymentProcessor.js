import { expect } from "chai";
import { ethers } from "hardhat";

const compare = (bad, good) => {
  console.table({
    bad: bad.toString(),
    good: good.toString(),
    saving: `${((bad - good) / bad * 100).toFixed(2)}%`,
  });

  expect(bad).to.be.greaterThan(good);
};

describe("Gas Optimizations", function () {
  async function deployFixture() {
    const [owner, merchant, user] = await ethers.getSigners();

    const PaymentProcessor = await ethers.getContractFactory("PaymentProcessor");
    const paymentProcessor = await PaymentProcessor.deploy();
    await paymentProcessor.waitForDeployment();

    // configuração básica do contrato (ajusta conforme seu construtor)
    await paymentProcessor.createPayment(
      merchant.address,
      ethers.parseEther("1.0")
    );

    return { paymentProcessor, owner, merchant, user };
  }

  it("Compare pay (external) vs payP (public)", async function () {
    const { paymentProcessor, user } = await deployFixture();

    // envia 1 ETH (ajusta conforme o createPayment define)
    const amount = ethers.parseEther("1.0");

    // --- pay() (external) ---
    const txExternal = await paymentProcessor.connect(user).pay(1, { value: amount });
    const receiptExternal = await txExternal.wait();

    // --- payP() (public) ---
    // recria um novo pagamento para comparar em igualdade de condições
    await paymentProcessor.createPayment(user.address, amount);
    const txPublic = await paymentProcessor.connect(user).payP(2, { value: amount });
    const receiptPublic = await txPublic.wait();

    // comparação de gas
    compare(receiptExternal.gasUsed, receiptPublic.gasUsed);
  });
});
