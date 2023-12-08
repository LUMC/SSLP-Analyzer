<?php
namespace App\Http\Livewire;

use Illuminate\Validation\Rule;
use Livewire\Component;

class AnalysisForm extends Component
{
    private $aData = [];
    private $aPopulations = [];
    private $aSSLPs = [];

    // Fields.
    public $nSSLP1;
    public $nSSLP2;
    public $nSSLP3;
    public $nSSLP4;
    public $sPopulation;

    public function __construct($id = null)
    {
        parent::__construct($id);

        // Open data JSON file.
        // FIXME: I'm currently unclear how to throw nice custom exceptions or so.
        //  Deliberately doing no checking at all.
        $sJSONFile = config('app.FSHD-path') . 'haplotypes.json';
        $this->aData = json_decode(file_get_contents($sJSONFile), true);

        // Fill in the list of populations.
        $this->aPopulations = array_keys($this->aData);
    }



    public function render()
    {
        // Render the component.

        // This wouldn't work in the __construct(), so I'll have to do it here.
        // When a population was selected in the form, we'd have that info now.
        $this->selectSSLPs();

        return view('livewire.analysis-form');
    }



    private function selectSSLPs()
    {
        // Fill in the list of SSLPs. We do this here because we may need to reload when a population has been selected.

        // When a population was selected in the form, select that one only and fetch population-specific lengths only.
        if ($this->sPopulation && isset($this->aData[$this->sPopulation])) {
            $this->aData = [$this->sPopulation => $this->aData[$this->sPopulation]];
        }
        foreach ($this->aData as $aChromosomes) {
            foreach ($aChromosomes as $aSizes) {
                $this->aSSLPs = array_unique(array_merge($this->aSSLPs, array_keys($aSizes)));
            }
        }
    }



    public function predict()
    {
        // Receives the data and runs a prediction.

        $this->selectSSLPs();
        $this->validate([
            'nSSLP1' => ['required', 'integer', Rule::in($this->aSSLPs)],
            'nSSLP2' => ['required', 'integer', Rule::in($this->aSSLPs)],
            'nSSLP3' => ['required', 'integer', Rule::in($this->aSSLPs)],
            'nSSLP4' => ['required', 'integer', Rule::in($this->aSSLPs)],
            'sPopulation' => ['required', Rule::in($this->aPopulations)],
        ]);

        // Call Python and collect result.
        $sLastLine = exec('python3 ' . escapeshellcmd(config('app.FSHD-path') . 'FSHD.py') . ' -s ' .
            implode(' ',
                array_map(
                    'escapeshellarg',
                    [
                        $this->nSSLP1,
                        $this->nSSLP2,
                        $this->nSSLP3,
                        $this->nSSLP4,
                    ])) . ' -p ' . escapeshellarg($this->sPopulation) . ' 2>&1', $aOutput, $nResult);

        if ($nResult) {
            // Something went wrong.
        } elseif (!$nResult && preg_match('/^No results found/', $aOutput[0])) {
            // No results.
            // $this->emitTo('AnalysisResults', 'setResults', []); // Doesn't work.
            $this->emit('setResults', []);
        } else {
            // Results.
            $aOutput = array_map(
                function ($sLine)
                {
                    return preg_split('/\s+/', $sLine);
                }, $aOutput
            );
            // $this->emitTo('analysis-results', 'setResults', $aOutput); // Doesn't work.
            $this->emit('setResults', $aOutput);
        }
    }
}
