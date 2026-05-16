import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Calculator, ShieldCheck, TrendingUp } from 'lucide-react';

const Hero = () => {
  return (
    <div className="relative bg-white overflow-hidden min-h-screen flex items-center pt-10">
      
      {/* Background Glowing Effects */}
      <div className="absolute top-0 right-0 -mr-32 -mt-32 w-96 h-96 rounded-full bg-brand-yellow opacity-10 blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 left-0 -ml-32 -mb-32 w-96 h-96 rounded-full bg-brand-navy opacity-10 blur-3xl"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center px-4 py-2 rounded-full bg-slate-50 text-brand-navy font-semibold text-sm mb-8 border border-slate-200 shadow-sm"
          >
            <ShieldCheck className="w-4 h-4 mr-2 text-brand-yellow" />
            Grow Wisely with Trusted Financial Experts
          </motion.div>

          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-5xl tracking-tight font-black text-brand-navy sm:text-6xl md:text-7xl leading-tight"
          >
            Smart Financial Solutions <br className="hidden md:block" />
            <span className="text-brand-yellow relative inline-block mt-2">
              For Your Future
            </span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-6 max-w-2xl mx-auto text-lg text-brand-grey sm:text-xl md:mt-8 font-medium"
          >
            Expert guidance on Home Loans, Business Loans, SIPs, and Loan Against Property. Build and secure your wealth with Addwise Financials.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="mt-10 sm:flex sm:justify-center gap-4"
          >
            {/* Primary Button */}
            <a href="#services" className="group w-full sm:w-auto flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-md text-white bg-brand-yellow hover:bg-brand-navy shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              Explore Services 
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>

            {/* External Calculator Button */}
            <a 
              href="http://addwisefin.investorcorner.co.in" 
              target="_blank" 
              rel="noopener noreferrer"
              className="mt-3 sm:mt-0 group w-full sm:w-auto flex items-center justify-center px-8 py-4 border-2 border-brand-navy text-lg font-bold rounded-md text-brand-navy bg-transparent hover:bg-brand-navy hover:text-white shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
            >
              Financial Calculators 
              <TrendingUp className="ml-2 w-5 h-5 group-hover:scale-110 transition-transform" />
            </a>
          </motion.div>

        </div>
      </div>
    </div>
  );
};

export default Hero;