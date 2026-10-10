import Dropdown from '../Components/DropDown';


export default function FrequencyResponse() {
   const signalUnits = [
    { label: 'V', onClick: () => console.log('Volts clicked') },
    { label: 'mV', onClick: () => console.log('Milivolts clicked') },
    { label: 'Pa', onClick: () => console.log('Pascals clicked') },
    { label: 'mPa', onClick: () => console.log('Milipascals clicked') },
  ];


  const timeUnits = [
    { label: 's', onClick: () => console.log('Seconds clicked') },
    { label: 'ms', onClick: () => console.log('Miliseconds clicked') },
    { label: 'µs', onClick: () => console.log('Microseconds clicked') },
  ];
  
return (
    <div>
      <h2>Frequency Response</h2>
      <p>Frequency response tools will go here.</p>

      <Dropdown title="Units" items={signalUnits} />
      <Dropdown title="Units" items={timeUnits} />
    </div>
  );
}