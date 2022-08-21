**Project Title :** Threat Hunting using Machine Learning Approaches in a Cloud Environment

**Abstract :**

One of the most significant technological revolutions of recent years hasbeen the shift to cloud computing.  When businesses switch to cloud technology, they can gain plenty of advantages.  This change can help save money while also improving how your employees interact.  Attacks now have the expertise to craft malicious applications disguised as legitimate tools. Unaware user’s and business organizations use such tools and compromise on their security. There are reactive approaches and proactive approaches to counter such attacks.  Security Information and Event Management  (SIEM),  firewalls,  anti-spam/anti-malware  solutions,  and  other  defences are employed in a reactive approach to cyber security, with the goal of  resolving  immediate  events  and  preventing  recurrent  attacks.   Systempatches  have  been  shown  to  have  serious  flaws  when  it  comes  to  dealing with contemporary attacks.  Vulnerability and penetration testing (VAPT)methodologies are acknowledged as having a limited scope and only working with threats that have previously been found.  Threat Hunting is one proactive  approach  that  has  become  a  significant  milestone  in  user  data protection.   In  this  project,  we  propose  a  machine  learning  approach  for threat hunting in a cloud environment which comprises of a malware detection framework which can detect new variants as well as malware’s hidden inside  begin  files  and  an  anomaly  detection  framework  which  is  capable  of identifying anomalies that occur in web logs and generate alerts to the endusers.

**Overview :**

Threat Hunting is a proactive approach towards securing a computer system.  It has been a significant milestone in user data protection in recent years century.  By actively searching, ”hunting”, for threats and making sure the computer system has no points of entry for an attack is an exhaustive but effective strategy for it’s protection.We propose such a model,  where a CNN model is deployed to a cloud environment and run periodically using a cron schedular.  The results generated from the model along with the logs generated by the cloud environment are stored in a storage bucket.  A tool for log analysis is used to analyse the reports generated.  A machine learning model for anomaly detection, also is used to detect anomalous network packets.  The outcome of the log analysis are used to formulate the result and alert the end user of the potential security risk or situation.
