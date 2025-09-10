import { FlatCompat } from '@eslint/eslintrc';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends(
    'next/core-web-vitals',
    'next/typescript',
    'eslint:recommended',
    '@typescript-eslint/recommended',
    '@typescript-eslint/recommended-requiring-type-checking'
  ),
  ...compat.config({
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 2023,
      sourceType: 'module',
      project: './tsconfig.json',
    },
    rules: {
      // === NAMING CONVENTIONS (ENFORCED) ===
      'check-file/filename-naming-convention': [
        'error',
        {
          '**/*.{ts,tsx}': 'KEBAB_CASE',
        },
        {
          ignoreMiddleExtensions: true,
        },
      ],
      '@typescript-eslint/naming-convention': [
        'error',
        // Variables and functions: camelCase
        {
          selector: 'variableLike',
          format: ['camelCase'],
        },
        {
          selector: 'functionLike',
          format: ['camelCase'],
        },
        // React components: PascalCase
        {
          selector: 'variable',
          filter: {
            regex: '^[A-Z].*Component$|^[A-Z][a-zA-Z]*$',
            match: true,
          },
          format: ['PascalCase'],
        },
        // Types and interfaces: PascalCase
        {
          selector: 'typeLike',
          format: ['PascalCase'],
        },
        // Constants: UPPER_CASE or camelCase
        {
          selector: 'variable',
          modifiers: ['const'],
          format: ['camelCase', 'UPPER_CASE'],
        },
        // Class members: camelCase
        {
          selector: 'classProperty',
          format: ['camelCase'],
        },
        {
          selector: 'classMethod',
          format: ['camelCase'],
        },
      ],

      // === CODE STYLE ===
      'prefer-arrow-callback': ['error'],
      'prefer-template': ['error'],
      'prefer-const': ['error'],
      semi: ['error', 'always'],
      quotes: ['error', 'single', { avoidEscape: true }],
      'comma-dangle': ['error', 'always-multiline'],
      'object-curly-spacing': ['error', 'always'],
      'array-bracket-spacing': ['error', 'never'],
      'key-spacing': ['error', { beforeColon: false, afterColon: true }],
      'space-before-blocks': ['error', 'always'],
      'keyword-spacing': ['error', { before: true, after: true }],

      // === TYPESCRIPT SPECIFIC ===
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/explicit-module-boundary-types': 'off',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/no-unnecessary-type-assertion': 'error',

      // === REACT/NEXT.JS SPECIFIC ===
      'react/prop-types': 'off', // Using TypeScript for props validation
      'react/react-in-jsx-scope': 'off', // Not needed in Next.js
      'react/display-name': 'error',
      'react/jsx-uses-react': 'off',
      'react/jsx-uses-vars': 'error',
      'react/jsx-key': 'error',
      'react/jsx-no-duplicate-props': 'error',
      'react/jsx-no-undef': 'error',
      'react/jsx-pascal-case': 'error',
      'react/no-children-prop': 'error',
      'react/no-danger-with-children': 'error',
      'react/no-deprecated': 'error',
      'react/no-direct-mutation-state': 'error',
      'react/no-find-dom-node': 'error',
      'react/no-is-mounted': 'error',
      'react/no-render-return-value': 'error',
      'react/no-string-refs': 'error',
      'react/no-unescaped-entities': 'error',
      'react/no-unknown-property': 'error',
      'react/require-render-return': 'error',
      'react/self-closing-comp': 'error',

      // === SECURITY ===
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-func': 'error',
      'no-script-url': 'error',

      // === PERFORMANCE ===
      'no-console': 'warn',
      'no-debugger': 'error',
      'no-alert': 'error',

      // === COMPLEXITY ===
      complexity: ['warn', 15],
      'max-depth': ['warn', 4],
      'max-lines': ['warn', 500],
      'max-params': ['warn', 5],

      // === IMPORTS ===
      'no-duplicate-imports': 'error',
      'import/no-duplicates': 'error',
      'import/no-unresolved': 'off', // TypeScript handles this
      'import/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
          ],
          'newlines-between': 'always',
          alphabetize: { order: 'asc', caseInsensitive: true },
        },
      ],
    },
  }),
  ...compat.plugins('check-file', '@typescript-eslint', 'import'),
];

export default eslintConfig;
