import * as React from 'react';

import './about.less';

const bbpLogo = require('../../assets/images/bbp-logo.jpeg');
const findLogo = require('../../assets/images/find-logo.png');
const connectionImage = require('../../assets/images/connection.png');

const About: React.FC = () => {
  return (
    <section className="about">
      <div className="half image-container">
        <img className="connection-image" src={connectionImage} />
        <div>
          <img className="bbp-logo" src={bbpLogo} />
          <img className="find-logo" src={findLogo} />
        </div>
      </div>
      <div className="half content">
        <h2 className="title underline">About</h2>
        <p>
          <span>
            <em>Mission statement/op-ed/Aim of project</em>
          </span>
          <br />
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Reiciendis
          beatae minima, sapiente doloremque odio repudiandae deleniti
          architecto unde cupiditate deserunt fugit adipisci aliquid, placeat
          inventore aut nam, quo cumque!
        </p>
        <p>
          <em>
            Collaborative effort between FIND and EPFL's Blue Brain Project
          </em>
          <br />
          <a>Add link here</a>
        </p>
      </div>
    </section>
  );
};

export default About;
