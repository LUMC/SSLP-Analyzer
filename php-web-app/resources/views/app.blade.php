<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{ env('APP_NAME') . ' v' . config('app.version') }}</title>

    <!-- Temporary solution to be able to use all of Tailwind without having to recompile it all the time -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.0.2/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>

    @livewireStyles
</head>
<body class="font-sans">
<div class="relative flex bg-blue-900 py-4">
    <div class="mx-auto pt-8">
        <div class="bg-white p-4 shadow rounded-lg">
            <div class="text-4xl font-bold">
                {{ env('APP_NAME') }}
            </div>
            <div>
                <livewire:analysis-form />

            </div>
            <div>
                <livewire:analysis-results />

            </div>
        </div>

        <div class="flex mt-4 justify-between text-sm text-blue-200">
            <div>
                {{ env('APP_NAME') . ' v' . config('app.version') }}
            </div>
            <div>
                built with Laravel v{{ Illuminate\Foundation\Application::VERSION }}
            </div>
        </div>
    </div>
</div>
@livewireScripts
</body>
</html>
