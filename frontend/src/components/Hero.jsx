import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Calculator } from 'lucide-react';

const Hero = () => {
  return (
    <div className="relative bg-white overflow-hidden min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="text-center">
          
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl"
          >
            <span className="block xl:inline">Smart Financial Solutions</span>{' '}
            <span className="block text-primary xl:inline">For Your Future</span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl"
          >
            Expert guidance on Home Loans, Business Loans, SIPs, and Loan Against Property. Build and secure your wealth with Addwise Financials.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8"
          >
            <div className="rounded-md shadow">
              <a href="#services" className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg transition-colors">
                Explore Services <ArrowRight className="ml-2 w-5 h-5" />
              </a>
            </div>
            <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
              {/* Yeh raha tumhara external calculator link */}
              <a 
                href="http://addwisefin.investorcorner.co.in" 
                target="_blank" 
                rel="noopener noreferrer"
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 md:py-4 md:text-lg transition-colors"
              >
                Financial Calculators <Calculator className="ml-2 w-5 h-5" />
              </a>
            </div>
          </motion.div>

        </div>
      </div>
    </div>
  );
};

export default Hero;