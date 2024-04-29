function WrapWithConditional(WrappedComponent) {

    return function ConditionalWrapper(props) {
  
      return (
        <>
          {
            !props.hasOwnProperty('displayCondition') || props.displayCondition
            ?
            <WrappedComponent {...props} />
            :
            null
          }
        </>
      )
  
    }
  
  }
  
  export default WrapWithConditional
  
  // TO USE: import the conditional wrapper into the component that it will wrap
  // and during export, wrap it in the function
  //
  // for example:
  //
  // import ConditionalWrapper from 'shared/ConditionalWrapper'
  //
  // `function App(){}`
  //
  // export default ConditionalWrapper(App);
  //
  //
  // conditional wrapper needs a displayCondition prop to work, otherwise it will
  // ignore it and display
  //
  // example:
  //
  // <App displayCondition={someBoolean} />
  