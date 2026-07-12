<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Route;
use File;

class ModuleServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        $modulesPath = app_path('Modules');
        if (!File::exists($modulesPath)) {
            return;
        }

        // Obtener la lista de nombres de carpetas de módulos
        $modules = array_map('basename', File::directories($modulesPath));

        foreach ($modules as $module) {
            // Cargar archivo de rutas si existe dentro del módulo
            $routeFile = $modulesPath . '/' . $module . '/Routes/api.php';
            if (File::exists($routeFile)) {
                Route::middleware(['api', 'throttle:60,1'])
                    ->prefix('api/v1/' . strtolower($module))
                    ->group($routeFile);
            }
        }
    }

    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }
}
