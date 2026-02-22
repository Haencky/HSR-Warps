export {};

declare global {
  interface Window {
    _env_: {
      BACKEND_URL: string;
    };
  }
}