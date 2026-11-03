import type { Config } from 'tailwindcss';
const config: Config = { content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'], theme: { extend: { colors: { ink: '#1d2528', paper: '#f7f6f2', muted: '#858b88', line: '#e7e5de', forest: '#34574b', gold: '#b38b55' }, boxShadow: { soft: '0 18px 55px rgba(35,42,38,.07)' } } }, plugins: [] };
export default config;
