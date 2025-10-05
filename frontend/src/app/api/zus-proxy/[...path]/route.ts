const TARGET_HOST = "https://www.zus.pl/";

export async function GET(req: Request) {
  const path = req.url?.replace("http://localhost:3000/api/zus-proxy/", "") || "";
  const proxiedUrl = `${TARGET_HOST}${path}`;
  console.log("fetching ", proxiedUrl);
  const response = await fetch(proxiedUrl, {
    mode: "no-cors",
    headers: {
      origin: TARGET_HOST,
      ...(req.headers as object),
    },
  });
  return response;
}
