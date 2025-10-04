import { SignIn } from "@/components/auth/signin-button";

export default function LoginPage() {
  return (
    <div className="bg-gray grid h-screen w-full place-items-center">
      <div className="flex flex-col items-center gap-0">
        {/* <h1 className="px-93.5 text-4xl font-semibold">Emerytownik ZUS</h1> */}

        <SignIn />
      </div>
    </div>
  );
}
