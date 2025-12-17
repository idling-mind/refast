import { default as React } from 'react';
import { ComponentTree } from './types';

declare global {
    interface Window {
        __REFAST_INITIAL_DATA__?: ComponentTree;
        __REFAST_CONFIG__?: {
            wsUrl?: string;
            csrfToken?: string;
        };
    }
}
interface RefastAppProps {
    initialTree?: ComponentTree;
    wsUrl?: string;
    className?: string;
}
/**
 * Main Refast application component.
 */
export declare function RefastApp({ initialTree, wsUrl, className }: RefastAppProps): React.ReactElement;
export default RefastApp;
