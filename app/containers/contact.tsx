import * as React from 'react';

import GetInTouchForm from '../components/GetInTouchForm';
import FAQ from '../components/FAQ';

const Contact: React.FC = () => {
  const handleGetInTouchForm = input => {
    console.log(input);
    // TODO do smth with it
  };

  return (
    <section className="contact">
      <div className="content">
        <h2 className="title underline">Contact</h2>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti,
          eaque recusandae. Incidunt unde praesentium omnis quasi dolorem, non,
          itaque alias fugiat facere hic tenetur, voluptatibus soluta laborum
          asperiores. Quia, ducimus.
        </p>
        <div className="container">
          <GetInTouchForm onSubmit={handleGetInTouchForm} />
        </div>
        <div className="container">
          <FAQ />
        </div>
        <div className="container">
          <em>User Feedback</em>
          <p>Coming soon</p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
