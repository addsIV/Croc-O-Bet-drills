// 集中管理環境設定。本機開發不設任何變數也能跑，所以給了 localhost 預設值。
export const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8787';
export const APP_ENV = import.meta.env.MODE;
