import React from 'react';
import { motion } from 'framer-motion';
import { Home, Briefcase, TrendingUp, Building } from 'lucide-react';

const servicesData = [
  {
    title: "Home Loan",
    description: "Turn your dream home into reality with our flexible and low-interest home loan solutions tailored for you.",
    icon: <Home className="w-8 h-8 text-brand-yellow" />,
  },
  {
    title: "Business Loan",
    description: "Fuel your business growth with quick approvals, minimal documentation, and competitive interest rates.",
    icon: <Briefcase className="w-8 h-8 text-brand-yellow" />,
  },
  {
    title: "SIP / Investment",
    description: "Build long-term wealth systematically. Get expert guidance on mutual funds and investment planning.",
    icon: <TrendingUp className="w-8 h-8 text-brand-yellow" />,
  },
  {
    title: "Loan Against Property",
    description: "Unlock the value of your property to meet your large financial needs with ease and convenience.",
    icon: <Building className="w-8 h-8 text-brand-yellow" />,
  }
];

const Services = () => {
  return (
    <section id="services" className="py-24 bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center mb-16">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl font-black text-brand-navy sm:text-4xl"
          >
            Our Premium Services
          </motion.h2>
          <motion.div 
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            className="w-24 h-1 bg-brand-yellow mx-auto mt-4 rounded-full"
          ></motion.div>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="mt-6 max-w-2xl text-lg text-brand-grey mx-auto font-medium"
          >
            Comprehensive financial solutions designed to secure your future and empower your dreams.
          </motion.p>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {servicesData.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -10 }}
              className="bg-white rounded-2xl p-8 shadow-sm border border-slate-100 hover:shadow-2xl transition-all duration-300 group"
            >
              <div className="w-16 h-16 bg-slate-50 group-hover:bg-brand-navy transition-colors duration-300 rounded-xl flex items-center justify-center mb-6 shadow-sm">
                {/* Icon color changes to white on hover */}
                <div className="group-hover:text-white transition-colors duration-300">
                  {service.icon}
                </div>
              </div>
              <h3 className="text-xl font-bold text-brand-navy mb-3 group-hover:text-brand-yellow transition-colors duration-300">
                {service.title}
              </h3>
              <p className="text-brand-grey leading-relaxed font-medium">
                {service.description}
              </p>
            </motion.div>
          ))}
        </div>

      </div>
    </section>
  );
};

export default Services;