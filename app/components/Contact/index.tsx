import * as React from 'react';

import GetInTouchForm from './GetInTouchForm';

import './contact.less';

const Contact: React.FC = () => {
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
          <GetInTouchForm />
        </div>
        <div className="container">
          <em>FAQ</em>
          <p>Coming soon</p>
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
