                <div>
@if(!isset($this->aResults))
@elseif(!$this->aResults)
                    No results for this combination.
@elseif(is_string($this->aResults))
                    <div class="w-full rounded-lg bg-red-200 ring-1 ring-red-500 p-2 px-3">
                        {{ $this->aResults }}
                    </div>
@else
                    <div class="bg-green-100 p-5 rounded-lg ring-1 ring-green-300">
                        <div class="overflow-x-auto bg-white rounded-lg ring-1 ring-green-900">
                            <table class="min-w-full text-left text-sm whitespace-nowrap">
                                <thead class="tracking-wider bg-green-900 text-white">
                                    <tr>
@foreach($this->aResults[0] as $sHeader)
                                        <th scope="col" class="px-6 py-4">
                                            {{ str_replace('(', ' (', $sHeader) }}
                                        </th>
@endforeach
                                    </tr>
                                </thead>
                                <tbody>
@foreach(array_slice($this->aResults, 1, count($this->aResults) - 2) as $aRow)
@php($nGreen = (round((int) $aRow[4] / 14) * 100))
@php($nGreenHover = min(((!$nGreen? -50 : $nGreen) + 100), 900))
@php($sTextColor = ($nGreen > 500? 'white' : 'black'))
                                    <tr class="border-b last:border-b-0 bg-green-{{ $nGreen }} text-{{ $sTextColor }} hover:bg-green-{{ $nGreenHover }}">
@foreach($aRow as $nRow => $sField)
                                        <td class="px-6 py-4">
                                            {{ $sField }}
                                        </td>
@endforeach
                                    </tr>
@endforeach
                                </tbody>
                            </table>
                        </div>
                        <div class="mt-2 text-sm text-green-800">
                            {{ implode(' ', $this->aResults[array_key_last($this->aResults)]) }}
                        </div>
                    </div>
@endif
                </div>
