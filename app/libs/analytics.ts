import Analytics from 'analytics';
import googleTagManager from '@analytics/google-tag-manager';

const enableAnalytics = () => {
  // TODO: move GTM code to env var at build-time
  const gtmCode = 'GTM-5J49535';

  if (gtmCode) {
    const analytics = Analytics({
      app: 'awesome-app',
      plugins: [
        googleTagManager({
          containerId: gtmCode,
        }),
      ],
    });

    analytics.page();
  }
};

export default enableAnalytics;
