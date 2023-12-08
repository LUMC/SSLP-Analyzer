module.exports = {
    purge: {
        content: [
            './resources/**/*.blade.php',
            './resources/**/*.js',
        ],
        safelist: [
            // These are styles that I apply in such a way, that their parser doesn't notice that I'm using them.
            // They get purged from the CSS file, and I need to prevent that by including them here.
            // Patterns are not supported in Tailwind 2.
            // {
            //     pattern: /bg-green-.+/,
            // }
            'bg-green-100',
            'bg-green-200',
            'bg-green-300',
            'bg-green-400',
            'bg-green-500',
            'bg-green-600',
            'bg-green-700',
            'bg-green-800',
            'bg-green-900',
            'hover:bg-green-50',
            'hover:bg-green-200',
            'hover:bg-green-300',
            'hover:bg-green-400',
            'hover:bg-green-500',
            'hover:bg-green-600',
            'hover:bg-green-700',
            'hover:bg-green-800',
            'hover:bg-green-900',
            'text-black',
            'text-white',
        ]
    },
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    variants: {
        extend: {
            // first: and last: are purged by default.
            // Prevent that by adding them here, specifically for the styles that use them.
            borderWidth: ['last'],
            padding: ['first', 'last'],
        }
    },
    plugins: [],
}
