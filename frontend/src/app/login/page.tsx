import { SignIn } from "@/components/auth/signin-button";

export default function LoginPage() {
  return (
    <div className="grid h-screen w-full place-items-center">
      <div className="flex flex-col items-center gap-4">
        Nie jesteś zalogowany 😔
        <SignIn />
      </div>
    </div>
  );
}
