import './css/App.css';
import './css/searchForm.css';

import Calendar from './components/calendar';
import SearchForm from './components/search';

function App() {
  return (
    <div className="App">
      <SearchForm />
      <Calendar />
    </div>
  );
}

export default App;
