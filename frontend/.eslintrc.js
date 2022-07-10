module.exports = {
    env: {
        browser: true,
        es2021: true,
    },
    extends: [
        "plugin:vue/vue3-recommended",
        "airbnb",
    ],
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
    },
    plugins: [
        "vue",
    ],
    rules: {
        quotes: ["error", "double"],
        indent: ["error", 4],
        "vue/html-indent": ["error", 4],
        "import/no-extraneous-dependencies": ["error", { devDependencies: ["vite.config.js"] }],
    },
};
