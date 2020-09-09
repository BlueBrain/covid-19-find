import * as React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const AwaitingInput: React.FC<{
  ready: boolean;
  loading: boolean;
  error: Error;
}> = ({ ready, loading, error }) => {
  return (
    <div className="action-box primary">
      <div className="title">
        <div className="number">
          <span>3</span>
        </div>
        <h2 className="underline">
          Visualize the <em>Simulation Model Results</em>
        </h2>
      </div>
      <div className="container">
        <p style={{ color: 'white' }}>
          Please complete the steps to view simulation results
        </p>
      </div>
      <div className="triangle primary">
        <div className={`loader ${loading ? 'loading' : ''}`}>
          <FontAwesomeIcon icon={faSpinner} pulse />
        </div>
      </div>
    </div>
  );
};

export default AwaitingInput;
