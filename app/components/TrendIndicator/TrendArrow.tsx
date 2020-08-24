import * as React from 'react';

const TrendArrow: React.FC<{ rotation: number }> = ({ rotation }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20.243"
      height="13.501"
      viewBox="0 0 20.243 13.501"
      style={{
        transform: `rotateZ(${rotation}deg)`,
      }}
    >
      <path
        id="Icon_ionic-ios-arrow-round-forward"
        data-name="Icon ionic-ios-arrow-round-forward"
        d="M20.784,11.51a.919.919,0,0,0-.007,1.294l4.275,4.282H8.782a.914.914,0,0,0,0,1.828H25.045L20.77,23.2a.925.925,0,0,0,.007,1.294.91.91,0,0,0,1.287-.007l5.794-5.836h0a1.026,1.026,0,0,0,.19-.288.872.872,0,0,0,.07-.352.916.916,0,0,0-.26-.64l-5.794-5.836A.9.9,0,0,0,20.784,11.51Z"
        transform="translate(-7.875 -11.252)"
      />
    </svg>
  );
};

export default TrendArrow;
