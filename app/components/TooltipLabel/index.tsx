import * as React from 'react';
import { IoIosInformationCircle } from 'react-icons/io';
import ReactTooltip from 'react-tooltip';
import tooltips from '../../tooltips';

const LabelWrapper = ({ children }) => <label>{children}</label>;

const TooltipLabel: React.FC<{
  tooltipKey: string;
  label: string | React.ReactNode;
  wrapper?: ({ children }: { children: any }) => JSX.Element;
}> = ({ tooltipKey, label, wrapper = LabelWrapper }) => {
  const tooltip = tooltips[tooltipKey];

  return tooltip ? (
    <>
      <a data-tip data-for={`${tooltipKey}-tooltip`}>
        {wrapper({
          children: (
            <>
              {label} <IoIosInformationCircle />
            </>
          ),
        })}
      </a>
      <ReactTooltip id={`${tooltipKey}-tooltip`}>
        <p>{tooltip}</p>
      </ReactTooltip>
    </>
  ) : (
    wrapper({ children: label })
  );
};

export default TooltipLabel;
