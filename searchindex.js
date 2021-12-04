Search.setIndex({docnames:["Data/constraint_dict","Data/controller_constraint","Data/data","Data/instance_data","Data/migration","Data/qos_constraint","Data/simulator","Model/analysis","Model/model","Model/optimizer","Model/parser","Model/round","Sim/bounded_pareto","Sim/gaussian","Sim/lognormal","Sim/simulation","Sim/simulator","Sim/weighted_gaussian","algorithms","exceptions","index","plotting","utils","validation"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["Data/constraint_dict.rst","Data/controller_constraint.rst","Data/data.rst","Data/instance_data.rst","Data/migration.rst","Data/qos_constraint.rst","Data/simulator.rst","Model/analysis.rst","Model/model.rst","Model/optimizer.rst","Model/parser.rst","Model/round.rst","Sim/bounded_pareto.rst","Sim/gaussian.rst","Sim/lognormal.rst","Sim/simulation.rst","Sim/simulator.rst","Sim/weighted_gaussian.rst","algorithms.rst","exceptions.rst","index.rst","plotting.rst","utils.rst","validation.rst"],objects:{"MigrationScheduling.Data":{ConstraintDict:[0,0,0,"-"],ControllerConstraint:[1,0,0,"-"],Migration:[4,0,0,"-"],QosConstraint:[5,0,0,"-"]},"MigrationScheduling.Data.ConstraintDict":{get_capacity:[0,2,1,""],get_load:[0,2,1,""],get_load_factor:[0,2,1,""],get_switches:[0,2,1,""],remove_switch:[0,2,1,""]},"MigrationScheduling.Data.ControllerConstraint":{add_switch:[1,2,1,""],get_cap:[1,2,1,""],get_controller:[1,2,1,""],get_controller_idx:[1,2,1,""],get_switches:[1,2,1,""]},"MigrationScheduling.Data.Migration":{add_qos_group:[4,2,1,""],get_dst_controller:[4,2,1,""],get_groups:[4,2,1,""],get_load:[4,2,1,""],get_switch:[4,2,1,""],get_switch_idx:[4,2,1,""],is_in_group:[4,2,1,""]},"MigrationScheduling.Data.QosConstraint":{add_switch:[5,2,1,""],get_cap:[5,2,1,""],get_group:[5,2,1,""],get_group_idx:[5,2,1,""],get_switches:[5,2,1,""]},"MigrationScheduling.Model":{Optimizer:[9,0,0,"-"],Parser:[10,0,0,"-"],Round:[11,0,0,"-"]},"MigrationScheduling.Model.Optimizer":{build_ip_model:[9,2,1,""],build_lp_model:[9,2,1,""],get_model_bounds:[9,2,1,""],get_model_data:[9,2,1,""],get_size_string:[9,2,1,""],instance_data:[9,2,1,""]},"MigrationScheduling.Model.Parser":{get_controller_constraints:[10,2,1,""],get_controller_ids:[10,2,1,""],get_group_ids:[10,2,1,""],get_migrations:[10,2,1,""],get_qos_constraints:[10,2,1,""],get_switch_ids:[10,2,1,""],parse_migrations:[10,2,1,""],to_data:[10,2,1,""]},"MigrationScheduling.Model.Round":{can_schedule_migration:[11,2,1,""],get_remaining_controller_capacities:[11,2,1,""],get_remaining_qos_capacities:[11,2,1,""],get_round_number:[11,2,1,""],get_scheduled_migrations:[11,2,1,""],print_migrations:[11,2,1,""],schedule_migration:[11,2,1,""]},"MigrationScheduling.Sim":{BoundedParetoSimulator:[12,0,0,"-"],GaussianSimulator:[13,0,0,"-"],LogNormalSimulator:[14,0,0,"-"],Simulator:[16,0,0,"-"],WeightedGaussianSimulator:[17,0,0,"-"]},"MigrationScheduling.Sim.Simulator":{Simulator:[16,1,1,""]},"MigrationScheduling.Sim.Simulator.Simulator":{run:[16,2,1,""]},"MigrationScheduling.algorithms":{calculate_migration_load:[18,3,1,""],current_bottleneck_first:[18,3,1,""],find_scheduling_round:[18,3,1,""],get_bottleneck_constraint:[18,3,1,""],get_bottleneck_migration:[18,3,1,""],remove_migration_from_constraints:[18,3,1,""],schedule_migration_in_earliest_round:[18,3,1,""],select_bottleneck_migration:[18,3,1,""],select_candidate_migrations:[18,3,1,""],vector_first_fit:[18,3,1,""]},"MigrationScheduling.analysis":{build_heuristics_string:[7,3,1,""],build_optimal_string:[7,3,1,""],build_results_string:[7,3,1,""],calculate_heuristic_results_for_instances:[7,3,1,""],calculate_optimal_results_for_instances:[7,3,1,""],compare_heuristic_results:[7,3,1,""],create_simulated_instances:[7,3,1,""],get_cores_and_instances_per_core:[7,3,1,""],get_deterioration_ratios:[7,3,1,""],get_deterioration_stats:[7,3,1,""],get_heuristic_discrepancy_df:[7,3,1,""],get_improvement_ratios:[7,3,1,""],get_improvement_stats:[7,3,1,""],get_instances_for_core:[7,3,1,""],get_proportion_better:[7,3,1,""],get_results_for_instances:[7,3,1,""],get_sim_tuples_for_core:[7,3,1,""],get_time_df:[7,3,1,""],initialize_and_join_processes:[7,3,1,""],load_results_df:[7,3,1,""],simulate_all_instances:[7,3,1,""],simulate_instance:[7,3,1,""],solve_instances_optimally:[7,3,1,""],write_optimal_results:[7,3,1,""],write_results_to_file:[7,3,1,""]},"MigrationScheduling.exceptions":{IncorrectBottleneckSetting:[19,4,1,""],InstanceNotSpecified:[19,4,1,""],InvalidName:[19,4,1,""],ModelNotOptimized:[19,4,1,""],SwitchNotFound:[19,4,1,""],UninitializedModel:[19,4,1,""]},"MigrationScheduling.plotting":{add_plot_formatting:[21,3,1,""],adjust_y_axis:[21,3,1,""],plot_results:[21,3,1,""],plot_results_comparison:[21,3,1,""],plot_runtimes:[21,3,1,""]},"MigrationScheduling.utils":{calculate_load_on_controller:[22,3,1,""],extract_file_idx:[22,3,1,""],gaussian_controller_capacity:[22,3,1,""],gaussian_qos_capacity:[22,3,1,""],get_all_files_by_pattern:[22,3,1,""],get_cap_dicts:[22,3,1,""],get_constraint_dict_for_controller:[22,3,1,""],get_constraint_dict_for_qos_group:[22,3,1,""],get_constraints_dict:[22,3,1,""],get_controller_cap_dict:[22,3,1,""],get_controller_constraint_dicts:[22,3,1,""],get_qos_constraint_dicts:[22,3,1,""],get_qos_group_cap_dict:[22,3,1,""],get_results_header:[22,3,1,""],initialize_seeds:[22,3,1,""],weighted_controller_capacity:[22,3,1,""],weighted_qos_capacity:[22,3,1,""]},"MigrationScheduling.validation":{validate_bottleneck_setting:[23,3,1,""],validate_name:[23,3,1,""]},MigrationScheduling:{Data:[2,0,0,"-"],Model:[8,0,0,"-"],Sim:[15,0,0,"-"],algorithms:[18,0,0,"-"],analysis:[7,0,0,"-"],exceptions:[19,0,0,"-"],plotting:[21,0,0,"-"],utils:[22,0,0,"-"],validation:[23,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:exception"},terms:{"0":[17,22],"1":[7,17,18,22],"2":[],"3":[17,22],"5":[],"6":17,"boolean":[9,21,22],"char":23,"class":[0,1,2,4,5,7,8,9,10,11,12,13,14,15,16,17,19],"default":[9,21,22],"float":[0,1,4,7,9,11,12,13,14,16,17,18,22],"function":[7,20,21,23],"int":[1,4,5,7,9,11,12,13,14,16,17,18,22],"new":18,"return":[0,1,4,5,7,9,10,11,16,18,21,22,23],"switch":[0,1,2,5,10,18,19,20],"true":[4,9,11,22],"while":[],A:[0,1,2,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23],At:18,For:[7,18],If:[0,1,4,9,18,22,23],In:18,It:[0,16],That:[0,7],The:[0,1,4,5,7,9,10,11,12,13,14,16,17,18,19,21,22,23],Then:7,These:7,_alpha:12,_bottleneck_typ:13,_capac:[0,1,5],_control:[1,12,13,14,16,17],_controller_const:[],_controller_constraint:10,_controller_id:[],_data:9,_dst_control:4,_group:[4,5],_load:[0,4],_low_prop:17,_med_prop:17,_migrat:[10,11,12,13,14,16,17],_model:9,_mu:14,_num_control:[12,13,14,16,17],_num_migr:[12,13,14,16,17],_num_qos_group:[12,13,14,16,17],_qos_const:[],_qos_constraint:10,_qos_group:[12,13,14,16,17],_qos_id:[],_rem_controller_cap:11,_rem_qos_cap:11,_round_id:[],_round_num:11,_sigma:14,_switch:[0,1,4,5],_switch_id:[],about:11,accept:[13,22],access:19,accommod:22,accomod:18,accord:[7,21],account:11,across:[0,7,21],activ:18,ad:[4,5,18,22],add:[1,4,5],add_plot_format:21,add_qos_group:4,add_switch:[1,5],addit:18,adjust:21,adjust_y_axi:21,after:[11,18],against:[7,21],algorithm:[7,20,22],all:[0,2,7,8,9,15,18,22],allow:[5,18,22],alpha:12,alreadi:18,also:[],among:18,amount:[11,22],an:[1,4,5,7,9,10,11,12,13,14,16,17,18,19,22,23],analyz:7,ani:18,anoth:18,appear:0,append:7,appli:[1,5,23],appropri:22,ar:[7,10,11,13,17,18,21,22,23],argument:7,associ:[0,18,22],attribut:[0,1,4,5,9,10,11,12,13,14,16,17],avail:18,averag:7,axi:21,base:[7,9,16,17,21,22],becom:[],been:[7,9,11,18,19],being:[0,4,7,9,11,19,21,23],belong:[4,11,12,13,14,16,17,18],best:[9,18],better:7,between:7,bin:18,bool:[4,7,9,11,21,22],both:[7,22],bottleneck:[7,13,17,18,19,22,23],bottleneck_const_nam:18,bottleneck_typ:[13,22],bound:[9,15,20,21],bound_i:21,boundedparetosimul:12,build:[1,7,9,19,22],build_heuristics_str:7,build_ip_model:9,build_lp_model:9,build_optimal_str:7,build_results_str:7,built:[10,22],calcul:[7,13,18,22],calculate_heuristic_results_for_inst:7,calculate_load_on_control:22,calculate_migration_load:18,calculate_optimal_results_for_inst:7,calculate_results_for_inst:[],can:[5,11,18,22],can_schedule_migr:11,candid:18,cannot:18,capac:[0,1,5,11,13,18,22],capciti:11,charact:23,check:4,chosen:18,collect:[0,1,4,5,7,10,18,21,22],column:[7,21,22],compact:[],compar:[7,21],compare_col:21,compare_heuristic_result:7,comparison:[7,21],complet:[7,9,11,22],comput:[7,9,21],concurr:5,consid:18,consist:22,constraint:[2,10,13,17,18,20,22],constraint_dict:18,constraintdict:[0,18,22],constraints_dict:18,constraintz:22,construct:[9,22],consts_dict:18,contain:[0,1,2,7,8,9,10,11,15,18,19,21,22],contigu:7,control:[2,4,9,10,11,12,13,14,16,17,18,20,22],control_const:22,controller_cap:[11,18],controller_const:[],controller_constraint:22,controller_id:[],controller_nam:22,controllerconstraint:[1,10,22],convent:23,convert:[],core:7,core_num:7,correct:[19,23],correspond:[1,7,10,11,18,21,22],count:7,creat:[7,10,18,21,22],create_simulated_inst:7,cumul:[],current:[7,11,18],current_bottleneck_first:18,cx:1,data:[0,1,4,5,9,10,18,20,21,22],datafram:[7,21],defin:[0,18],degre:0,denot:[7,18],depend:22,desir:[],destin:[4,10,11,12,13,14,16,17,18,22],detail:[4,19],deterior:7,determin:11,deviat:[7,14],df:7,dict:[7,10,11,18,22],dictionari:[2,7,10,11,18,20,22],differ:7,directli:[],directori:[7,22],discrep:7,displai:19,distinct:7,distribut:[12,13,14,16,17,22],divid:[0,18],doe:[18,23],done:7,dst_control:4,dure:[4,9],each:[7,11,12,13,14,16,17,18,21,22],earliest:18,element:[7,12,13,14,16,17],enough:18,ensur:23,entir:9,equal:[7,18],error:23,exactli:22,exceed:11,except:20,exclud:18,exclude_const:18,exist:18,existing_round:18,experi:[21,22],experiment:7,explicit:21,ext:22,extens:22,extract:22,extract_file_idx:22,factor:[0,22],fals:[4,11,21],fewer:7,file:[7,9,10,16,21,22],file_dir:22,file_pattern:[7,22],filenam:7,find:[7,18],find_scheduling_round:18,first:[7,12,13,14,16,17,18,22,23],first_lett:23,fit:[7,18],follow:[7,9,23],form:[1,4,22],format:21,formula:[],found:[9,19],from:[0,5,7,10,11,17,18,21,22],g:18,gaussian:[15,20,22],gaussian_controller_capac:22,gaussian_qos_capac:22,gaussiansimul:13,gener:[7,13,19,22],generate_controller_capac:[],generate_qos_capac:[],get:[7,22],get_all_files_by_pattern:22,get_bottleneck_constraint:18,get_bottleneck_migr:18,get_cap:[1,5],get_cap_dict:22,get_capac:0,get_constraint_dict:[],get_constraint_dict_for_control:22,get_constraint_dict_for_qos_group:22,get_constraints_dict:22,get_control:1,get_control_const:[],get_controller_cap_dict:22,get_controller_constraint:10,get_controller_constraint_dict:22,get_controller_id:10,get_controller_idx:1,get_cores_and_instances_per_cor:7,get_deterioration_ratio:7,get_deterioration_stat:7,get_dst_control:4,get_group:[4,5],get_group_id:10,get_group_idx:5,get_heuristic_discrepancy_df:7,get_improvement_ratio:7,get_improvement_stat:7,get_instances_for_cor:7,get_load:[0,4],get_load_factor:0,get_log_mean:[],get_log_std:[],get_migr:10,get_model_bound:9,get_model_data:9,get_proportion_bett:7,get_qos_const:[],get_qos_constraint:10,get_qos_constraint_dict:22,get_qos_group_cap_dict:22,get_qos_id:[],get_remaining_controller_capac:11,get_remaining_qos_capac:11,get_results_for_inst:7,get_results_head:22,get_round_id:[],get_round_numb:11,get_round_reduction_stat:[],get_scheduled_migr:11,get_sim_tuples_for_cor:7,get_size_str:9,get_switch:[0,1,4,5],get_switch_id:10,get_switch_idx:4,get_time_df:7,get_total_load:[],given:[7,11,17,18],greater:7,group:[4,5,7,9,10,11,12,13,14,16,17,18,22],group_col:7,group_nam:4,group_siz:22,gurobi:9,gurobipi:9,ha:[1,4,7,9,18,19],handl:[11,18,22],have:[7,11,18,21,22],header:22,help:7,heurist:[7,18,22],heuristic1:7,heuristic2:7,heuristic_col:7,high:[7,13,17,19,22,23],highest:18,hold:[0,7],id:[1,4,10],identifi:[0,4,7,22],idx:22,ignor:18,ilp:[],implement:[18,21,23],impos:22,improv:7,includ:7,incorrect:19,incorrectbottleneckset:[19,23],incur:[0,4,12,13,14,16,17],index:[1,4,5,7,18,20,21,22],indic:[9,11,18,21,22],individu:13,info:0,inform:[0,1,4,5,11],initi:[7,9,19,22,23],initialize_and_join_process:7,initialize_se:22,input_dir:7,inspir:18,instanc:[2,7,8,9,10,12,13,14,15,16,17,18,19,20,22],instance_count:7,instance_data:[7,9,18,22],instance_fil:[7,22],instance_idx:7,instance_s:7,instancedata:[7,9,10,18,22],instancenotspecifi:[9,19],instances_per_cor:7,instanti:9,integ:[1,4,5,7,9,10,11,12,13,14,16,17,18,22,23],interest:7,invalid:19,invalidnam:[1,4,19,23],involv:[4,10,18],is_in_group:4,iter:18,its:[11,18],join:7,just:7,kei:[7,10,11,18,22],less:7,level:7,lh:0,likewis:7,line:[7,21],linear:9,list:[7,10,12,13,14,16,17,18,21,22],ln:[],load:[0,2,4,7,8,9,11,12,13,14,15,16,17,18,19,22],load_results_df:7,locat:7,loda:16,log:[15,20],log_scal:21,logarithm:21,lognorm:14,lognormalsimul:14,loop:18,low:[13,17,19,22,23],low_prop:[17,22],lower:[9,21],machin:7,maintain:18,make:21,manag:7,match:22,max_cap:22,maximum:[5,7,11,12,13,14,16,17,18,22],mean:[7,14],med_prop:[17,22],medium:[13,17,19,22,23],member:4,messag:[9,19],method1:7,method2:7,method:[0,1,4,5,7,9,10,11,12,13,14,16,17],migrat:[0,1,5,7,8,9,10,12,13,14,15,16,17,18,19,22],migration_fil:[9,10],migrationschedul:[0,1,4,5,7,9,10,11,12,13,14,16,17,18,19,21,22,23],min_cap:22,minimum:[7,22],minu:11,mode:9,model:[9,10,11,19,20,22],modelnotoptim:19,modul:[2,7,8,15,18,19,20,21,22,23],more:7,most:18,mp:7,mu:14,multiprocess:7,name:[0,1,4,5,7,10,11,16,18,19,21,22,23],need:1,none:[0,1,4,5,7,9,10,11,16,18,21,22,23],normal:[15,20],num_candid:18,num_choic:18,num_migr:16,num_round:18,number:[5,7,9,11,12,13,14,16,17,18,22],object:[1,7,9,10,11,12,13,14,16,17,18,19,22,23],object_typ:23,obtain:[7,18],one:[7,9,17,18,19,22,23],onli:9,opt_col:7,optim:[7,8,19,20,22],origin:11,other:[7,18],otherwis:[4,7,9,11],outperform:7,output:[7,16,21],output_dir:7,output_fil:[7,16,21],output_idx:7,over:7,overload:0,pack:18,page:20,panda:[7,21],paramet:[0,1,4,5,7,9,10,11,12,13,14,16,17,18,19,21,22,23],pareto:[15,20],pars:[9,10],parse_migr:10,parser:[8,9,20],part:4,pass:7,path:9,pattern:[7,22],pd:[7,21],per:[7,9,18],percent:7,percentag:7,perform:[4,7,21],pick:22,place:5,plot:20,plot_result:21,plot_result_v:[],plot_results_comparison:21,plot_runtim:21,point:22,posit:12,possibl:18,pre:9,print:[9,11,21],print_migr:11,problem:[0,7,9,11,18],proc:7,process:7,program:9,proper:23,properli:23,proport:[7,17,22],proposed_nam:23,qo:[2,4,9,10,11,12,13,14,16,17,18,20,22],qos_cap:[11,18],qos_const:22,qos_constraint:22,qos_id:[],qosconstraint:[5,10,22],qoscontraint:10,queri:19,rais:[0,1,4,9,19,23],random:[17,22],rang:[17,22],ratio:7,read:7,record:7,reduc:0,reduct:[],reflect:18,rel:[18,22],relat:[4,5,11,23],remain:[11,18],remov:[0,18],remove_migration_from_constraint:18,remove_switch:0,report:7,repres:[0,1,4,5,7,9,10,11,12,13,14,16,17,18,19,21,22,23],represent:[],reproduc:22,requir:7,respect:[],restrict:7,result:[7,21,22],result_col:21,result_idx:7,results_col:21,results_df:[7,21],results_fil:7,results_list:7,retriev:[7,9,22],rh:0,roughli:7,round:[0,7,8,9,18,20,22],round_id:[],round_num:11,run:[7,16,18,22],run_optim:[7,22],runtim:21,s:[1,18,21],same:[7,18],sampl:[17,18,22],sample_with_log_op:[],scale:21,schedul:[0,7,8,9,11,12,13,14,15,16,17,19,22],schedule_migr:11,schedule_migration_in_earliest_round:18,sdn:4,search:[19,20,22],second:[7,12,13,14,16,17,22],seed:22,seed_num:22,select:18,select_bottleneck_migr:18,select_candidate_migr:18,select_migration_from_constraint:[],separ:[7,9,22],serv:16,set:[0,1,4,5,10,11,13,17,18,19,22,23],shape:12,should:[4,18,21],sigma:14,signal:[18,23],signifi:[4,18],sim:[12,13,14,16,17],sim_arg:7,sim_cl:7,sim_tupl:7,sims_per_cor:7,simul:[7,20],simulate_all_inst:7,simulate_inst:7,simultan:5,singl:[0,11,18,22],size:[7,9,22],so:7,solut:[7,9,22],solv:[7,9,18,22],solve_instances_optim:7,sort:7,sort_col:7,sourc:[0,1,4,5,7,9,10,11,12,13,14,16,17,18,19,21,22,23],space:[7,9,22],specif:16,specifi:[7,9,10,12,13,14,16,17,18,19,22],sqrt:[],standard:[14,21],start:7,start_idx:7,statist:7,store:[1,2,4,5,11,22],str:[0,1,4,5,7,9,10,13,16,18,19,21,22,23],string:[0,1,4,5,7,9,10,11,13,16,18,19,21,22,23],subset:[7,22],sum:[11,16,18,22],suppli:19,supplied_set:[19,23],switch_id:[],switch_load:0,switch_nam:[0,1,5,19],switchnotfound:[0,19],sx:4,system:7,take:[5,9],taken:[7,22],than:7,thi:[0,4,7,12,13,14,16,17,18,21,23],third:16,those:7,three:[16,17],through:[18,22],time:[7,17],time_col:7,time_var:21,titl:21,to_data:10,total:0,transit:[],tri:19,tupl:[7,12,13,14,16,17],two:[7,12,13,14,17,22],type:7,underli:14,uninitializedmodel:19,updat:[10,18],upper:[9,21],upper_bound_round:[],us:[0,1,2,4,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23],user:19,util:20,valid:[1,4,20],validate_bottleneck_set:23,validate_nam:23,valu:[1,7,9,10,11,12,13,18,21,22],variabl:[7,21],variou:7,vector:[7,18],vector_first_fit:18,verbos:9,version:18,visual:21,we:18,weight:[15,20,22],weighted_controller_capac:22,weighted_qos_capac:22,weightedgaussiansimul:17,well:7,were:0,when:[4,7,18,19],where:[1,4,7,22],whether:[7,9,11,21,22,23],which:[0,1,4,5,7,16,18,21,22,23],within:[5,22],without:11,work:8,wors:7,would:0,write:7,write_optimal_result:7,write_results_to_fil:7,written:7,x:[1,4,7,21],x_titl:21,x_var:21,y:21,y_titl:21,yet:[9,19]},titles:["Constraint Dictionary","Controller Constraint","Migration Scheduling Data","Instance Data","Switch Migration","QoS Constraint","Migration Simulator","Analysis","Model","Optimizer","Parser","Migration Round","Bounded Pareto Simulator","Gaussian Simulator","Log Normal Simulator","Simulation","Simulator","Weighted Gaussian Simulator","Scheduling Algorithms","Exceptions","Welcome to Load Migration Scheduling\u2019s documentation!","Plotting","Utility Functions","Validation"],titleterms:{"function":22,"switch":4,algorithm:18,analysi:7,bound:12,constraint:[0,1,5],control:1,data:[2,3],dictionari:0,document:20,except:19,gaussian:[13,17],indic:20,instanc:3,load:20,log:14,migrat:[2,4,6,11,20],model:8,normal:14,optim:9,pareto:12,parser:10,plot:21,qo:5,round:11,s:20,schedul:[2,18,20],simul:[6,12,13,14,15,16,17],tabl:20,util:22,valid:23,weight:17,welcom:20}})