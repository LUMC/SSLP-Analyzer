<?php

namespace App\Http\Livewire;

use Livewire\Component;

class AnalysisResults extends Component
{
    public $aResults = null;

    protected $listeners = ['setResults'];

    public function render()
    {
        return view('livewire.analysis-results');
    }

    public function setResults ($aResults)
    {
        $this->aResults = $aResults;
    }
}
