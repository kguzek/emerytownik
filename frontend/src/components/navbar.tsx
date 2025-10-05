import Image from "next/image";
import Link from "next/link";

import zusLogo from "@/../public/logo_zus_darker_with_text.svg";

export function Navbar() {
  return (
    <div className="flex h-26.5 w-full flex-col pt-6">
      <Link href="/zus.html" className="mx-3.5">
        <Image alt="zus logo" src={zusLogo} height={55} width={250} />
      </Link>
      <div className="bg-gray/40 mt-5 h-full w-full"></div>
    </div>
  );
}
