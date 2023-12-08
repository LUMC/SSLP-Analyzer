                <div>
                    <form wire:submit.prevent="predict">
                        <div class="flex justify-between">
                            <div class="py-2 sm:px-1 md:px-2 first:pl-0 last:pr-0">
                                <select name="population" id="population" wire:model.lazy="sPopulation" class="rounded-md p-2 sm:px-2 md:px-4 bg-sky-100 shadow-sm ring-1 ring-inset ring-sky-300 sm:text-sm md:text-base @error('sPopulation') bg-rose-300 ring-red-600 @enderror">
                                    <option value="">(Population)</option>
                                    @foreach($this->aPopulations as $sPopulation)
                                        <option value="{{ $sPopulation }}">{{ $sPopulation }}</option>
                                    @endforeach
                                </select>
                            </div>
@for ($i = 1; $i <= 4; $i++)
                                <div class="py-2 sm:px-1 md:px-2 first:pl-0 last:pr-0">
                                    <select name="SSLP{{ $i }}" id="SSLP{{ $i }}" wire:model.defer="nSSLP{{ $i }}" class="rounded-md p-2 sm:px-2 md:px-4 bg-sky-100 shadow-sm ring-1 ring-inset ring-sky-300 sm:text-sm md:text-base @error('nSSLP' . $i) bg-rose-300 ring-red-600 @enderror">
                                        <option value="">(SSLP size)</option>
@foreach($this->aSSLPs as $nSSLP)
                                        <option value="{{ $nSSLP }}">{{ $nSSLP }}</option>
@endforeach
                                    </select>
                                </div>
@endfor
                            <div class="py-2 sm:px-1 md:px-2 first:pl-0 last:pr-0">
                                <input type="submit" value="Predict" class="rounded-md p-2 sm:px-2 md:px-4 bg-blue-800 text-white font-bold shadow-sm ring-1 ring-inset ring-blue-900 sm:text-sm md:text-base">
                            </div>
                        </div>
                    </form>
                </div>
