import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
async function main() {
  const konrad = await prisma.user.upsert({
    where: { email: "konrad@solvro.pl" },
    update: {},
    create: {
      email: "konrad@solvro.pl",
      name: "Konrad",
    },
  });
  console.log({ konrad });
}
main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
