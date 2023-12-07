<?php
namespace App\Http\Livewire;

use Illuminate\Validation\Rule;
use Livewire\Component;

class AnalysisForm extends Component
{
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
        $aData = json_decode(file_get_contents($sJSONFile), true);

        // Fill in the list of populations.
        $this->aPopulations = array_keys($aData);

        // Fill in the list of SSLPs.
        foreach ($aData as $sPop => $aChromosomes) {
            foreach ($aChromosomes as $sChromosome => $aSizes) {
                $this->aSSLPs = array_unique(array_merge($this->aSSLPs, array_keys($aSizes)));
            }
        }
    }

    public function render()
    {
        return view('livewire.analysis-form');
    }

    public function predict()
    {
        // Receives the data and runs a prediction.

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
