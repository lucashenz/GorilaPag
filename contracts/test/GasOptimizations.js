import {
    time,
    loadFixture,
} from "@nomicfoundation/hardhat-network-helpers";
import { anyValue } from "@nomicfoundation/hardhat-chai-matchers/withArgs";
import { expect } from "chai";
import { ethers } from "hardhat";

const compare = (bad, good) => {
  console.table({
    bad: bad.toString(),
    good: good.toString(),
    saving: `${((bad - good) / bad * 100).toFixed(2)}%`
  });

  expect(bad).to.be.greaterThan(good);
};

describe("Gas Optimizations", function () {
  it("Compare External vs Public", async function () {
    const GasOptimizations = await ethers.getContractFactory("smartContracts/PaymentProcessor");
    const gasOptimizations = await GasOptimizations.deploy();
    await gasOptimizations.waitForDeployment();

    // Exemplo de medição de gas entre funções external e public
    const txExternal = await gasOptimizations.callExternal();
    const receiptExternal = await txExternal.wait();

    const txPublic = await gasOptimizations.callPublic();
    const receiptPublic = await txPublic.wait();

    compare(
      receiptExternal.gasUsed,
      receiptPublic.gasUsed
    );
  });
});
