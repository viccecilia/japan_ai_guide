import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Japan AI Guide",
  description: "ChatGPT-style AI guide platform for travel in Japan.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
