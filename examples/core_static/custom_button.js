(function() {
  const { componentRegistry, React } = window.RefastClient;

  const CustomButton = (props) => {
    // React.createElement signature: type, props, ...children
    return React.createElement(
      'button',
      {
        onClick: props.onClick,
        className: 'px-6 py-3 rounded-lg font-semibold text-white bg-indigo-600 hover:bg-indigo-700 shadow-md hover:shadow-lg active:scale-95 transition-all duration-150 ' + (props.className || '')
      },
      props.label || props.children || 'Custom Action'
    );
  };

  componentRegistry.register('CustomButton', CustomButton);
})();
