# example call for standalone file
input=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Batch_Analysis_stage1
output=/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/flatNtuples/spring2021/prod_04/Analysis_stage2
ana=examples/FCCee/flavour/Bc2TauNu/analysis_stage2.py


#for process in p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU;
for process in p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTau23PiPi0NuTAUOLA;
do
    python $ana $output/$process.root "$input/$process/*.root"
done

