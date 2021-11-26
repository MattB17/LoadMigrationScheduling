Search.setIndex({docnames:["Data/constraint_dict","Data/controller_constraint","Data/data","Data/instance_data","Data/migration","Data/qos_constraint","Data/simulator","Model/analysis","Model/model","Model/optimizer","Model/parser","Model/round","Sim/gaussian","Sim/lognormal","Sim/simulation","Sim/simulator","algorithms","exceptions","index","plotting","utils","validation"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["Data/constraint_dict.rst","Data/controller_constraint.rst","Data/data.rst","Data/instance_data.rst","Data/migration.rst","Data/qos_constraint.rst","Data/simulator.rst","Model/analysis.rst","Model/model.rst","Model/optimizer.rst","Model/parser.rst","Model/round.rst","Sim/gaussian.rst","Sim/lognormal.rst","Sim/simulation.rst","Sim/simulator.rst","algorithms.rst","exceptions.rst","index.rst","plotting.rst","utils.rst","validation.rst"],objects:{"MigrationScheduling.Data":{ConstraintDict:[0,0,0,"-"],ControllerConstraint:[1,0,0,"-"],Migration:[4,0,0,"-"],QosConstraint:[5,0,0,"-"]},"MigrationScheduling.Data.ConstraintDict":{get_capacity:[0,2,1,""],get_load:[0,2,1,""],get_load_factor:[0,2,1,""],get_switches:[0,2,1,""],remove_switch:[0,2,1,""]},"MigrationScheduling.Data.ControllerConstraint":{add_switch:[1,2,1,""],get_cap:[1,2,1,""],get_controller:[1,2,1,""],get_controller_idx:[1,2,1,""],get_switches:[1,2,1,""]},"MigrationScheduling.Data.Migration":{add_qos_group:[4,2,1,""],get_dst_controller:[4,2,1,""],get_groups:[4,2,1,""],get_load:[4,2,1,""],get_switch:[4,2,1,""],get_switch_idx:[4,2,1,""],is_in_group:[4,2,1,""]},"MigrationScheduling.Data.QosConstraint":{add_switch:[5,2,1,""],get_cap:[5,2,1,""],get_group:[5,2,1,""],get_group_idx:[5,2,1,""],get_switches:[5,2,1,""]},"MigrationScheduling.Model":{Optimizer:[9,0,0,"-"],Parser:[10,0,0,"-"],Round:[11,0,0,"-"]},"MigrationScheduling.Model.Optimizer":{build_ip_model:[9,2,1,""],build_lp_model:[9,2,1,""],get_model_bounds:[9,2,1,""],get_model_data:[9,2,1,""],get_size_string:[9,2,1,""],instance_data:[9,2,1,""]},"MigrationScheduling.Model.Parser":{get_controller_constraints:[10,2,1,""],get_controller_ids:[10,2,1,""],get_group_ids:[10,2,1,""],get_migrations:[10,2,1,""],get_qos_constraints:[10,2,1,""],get_switch_ids:[10,2,1,""],parse_migrations:[10,2,1,""],to_data:[10,2,1,""]},"MigrationScheduling.Model.Round":{can_schedule_migration:[11,2,1,""],print_migrations:[11,2,1,""],schedule_migration:[11,2,1,""]},"MigrationScheduling.Sim":{GaussianSimulator:[12,0,0,"-"],LogNormalSimulator:[13,0,0,"-"],Simulator:[15,0,0,"-"]},"MigrationScheduling.Sim.Simulator":{Simulator:[15,1,1,""]},"MigrationScheduling.Sim.Simulator.Simulator":{run:[15,2,1,""]},"MigrationScheduling.algorithms":{calculate_migration_load:[16,3,1,""],current_bottleneck_first:[16,3,1,""],find_scheduling_round:[16,3,1,""],get_bottleneck_constraint:[16,3,1,""],get_bottleneck_migration:[16,3,1,""],remove_migration_from_constraints:[16,3,1,""],schedule_migration_in_earliest_round:[16,3,1,""],select_bottleneck_migration:[16,3,1,""],select_candidate_migrations:[16,3,1,""],vector_first_fit:[16,3,1,""]},"MigrationScheduling.analysis":{build_heuristics_string:[7,3,1,""],build_optimal_string:[7,3,1,""],build_results_string:[7,3,1,""],calculate_results_for_instances:[7,3,1,""],compare_heuristic_results:[7,3,1,""],create_simulated_instances:[7,3,1,""],get_cores_and_instances_per_core:[7,3,1,""],get_heuristic_discrepancy_df:[7,3,1,""],get_instances_for_core:[7,3,1,""],get_proportion_better:[7,3,1,""],get_results_for_instances:[7,3,1,""],get_round_reduction_stats:[7,3,1,""],get_sim_tuples_for_core:[7,3,1,""],get_time_df:[7,3,1,""],initialize_and_join_processes:[7,3,1,""],load_results_df:[7,3,1,""],simulate_all_instances:[7,3,1,""],simulate_instance:[7,3,1,""],write_results_to_file:[7,3,1,""]},"MigrationScheduling.exceptions":{IncorrectBottleneckSetting:[17,4,1,""],InstanceNotSpecified:[17,4,1,""],InvalidName:[17,4,1,""],ModelNotOptimized:[17,4,1,""],SwitchNotFound:[17,4,1,""],UninitializedModel:[17,4,1,""]},"MigrationScheduling.plotting":{add_plot_formatting:[19,3,1,""],adjust_y_axis:[19,3,1,""],plot_results:[19,3,1,""],plot_results_comparison:[19,3,1,""],plot_runtimes:[19,3,1,""]},"MigrationScheduling.utils":{calculate_load_on_controller:[20,3,1,""],generate_controller_capacity:[20,3,1,""],generate_qos_capacity:[20,3,1,""],get_all_files_by_pattern:[20,3,1,""],get_cap_dicts:[20,3,1,""],get_constraint_dict_for_controller:[20,3,1,""],get_constraint_dict_for_qos_group:[20,3,1,""],get_constraints_dict:[20,3,1,""],get_controller_cap_dict:[20,3,1,""],get_controller_constraint_dicts:[20,3,1,""],get_log_mean:[20,3,1,""],get_log_std:[20,3,1,""],get_qos_constraint_dicts:[20,3,1,""],get_qos_group_cap_dict:[20,3,1,""],get_results_header:[20,3,1,""],initialize_seeds:[20,3,1,""],sample_with_log_op:[20,3,1,""]},"MigrationScheduling.validation":{validate_bottleneck_setting:[21,3,1,""],validate_name:[21,3,1,""]},MigrationScheduling:{Data:[2,0,0,"-"],Model:[8,0,0,"-"],Sim:[14,0,0,"-"],algorithms:[16,0,0,"-"],analysis:[7,0,0,"-"],exceptions:[17,0,0,"-"],plotting:[19,0,0,"-"],utils:[20,0,0,"-"],validation:[21,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","function","Python function"],"4":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:function","4":"py:exception"},terms:{"0":20,"1":[7,16],"2":20,"5":20,"boolean":[7,9,19,20],"char":21,"class":[0,1,2,4,5,7,8,9,10,11,12,13,14,15,17],"default":[9,19,20],"float":[0,1,4,7,9,11,12,13,15,16,20],"function":[7,18,19,21],"int":[1,4,5,7,9,11,12,13,15,16,20],"new":16,"return":[0,1,4,5,7,9,10,11,15,16,19,20,21],"switch":[0,1,2,5,10,16,17,18],"true":[4,7,9,11,20],"while":[],A:[0,1,2,4,5,7,8,9,10,11,12,13,14,15,16,17,19,20,21],At:16,For:[7,16],If:[0,1,4,7,9,16,20,21],In:16,It:[0,15],That:[0,7],The:[0,1,4,5,7,9,10,11,12,13,15,16,17,19,20,21],Then:7,_bottleneck_typ:12,_capac:[0,1,5],_control:[1,12,13,15],_controller_const:[],_controller_constraint:10,_controller_id:[],_data:9,_dst_control:4,_group:[4,5],_load:[0,4],_migrat:[10,11,12,13,15],_model:9,_mu:13,_num_control:[12,13,15],_num_migr:[12,13,15],_num_qos_group:[12,13,15],_qos_const:[],_qos_constraint:10,_qos_group:[12,13,15],_qos_id:[],_rem_controller_cap:11,_rem_qos_cap:11,_round_id:[],_round_num:11,_sigma:13,_switch:[0,1,4,5],_switch_id:[],about:11,accept:[12,20],access:17,accommod:20,accomod:16,accord:[7,19,20],account:11,across:[0,7,19],activ:16,ad:[4,5,16,20],add:[1,4,5],add_plot_format:19,add_qos_group:4,add_switch:[1,5],addit:16,adjust:19,adjust_y_axi:19,after:[11,16],against:[7,19],algorithm:[7,18,20],all:[0,2,7,8,9,14,16,20],allow:[5,16,20],alreadi:16,also:7,among:16,amount:[11,20],an:[1,4,5,7,9,10,11,12,13,15,16,17,20,21],analyz:7,ani:16,anoth:16,appear:0,append:7,appli:[1,5,21],appropri:20,ar:[7,10,11,12,16,19,20,21],argument:7,associ:[0,16,20],attribut:[0,1,4,5,9,10,11,12,13,15],avail:16,averag:7,axi:19,base:[7,9,15,19,20],becom:20,been:[7,9,16,17],being:[0,4,7,9,11,17,19,21],belong:[4,12,13,15,16],best:[9,16],between:7,bin:16,bool:[4,7,9,11,19,20],both:[7,20],bottleneck:[7,12,16,17,20,21],bottleneck_const_nam:16,bottleneck_typ:[12,20],bound:[9,19],bound_i:19,build:[1,7,9,17,20],build_heuristics_str:7,build_ip_model:9,build_lp_model:9,build_optimal_str:7,build_results_str:7,built:[10,20],calcul:[7,12,16,20],calculate_load_on_control:20,calculate_migration_load:16,calculate_results_for_inst:7,can:[5,7,11,16,20],can_schedule_migr:11,candid:16,cannot:16,capac:[0,1,5,11,12,16,20],capciti:11,charact:21,check:4,chosen:16,collect:[0,1,4,5,7,10,16,19,20],column:[7,19,20],compact:[],compar:[7,19],compare_col:19,compare_heuristic_result:7,comparison:[7,19],complet:[7,9,11,20],comput:[7,9,19],concurr:5,consid:16,consist:20,constraint:[2,10,12,16,18,20],constraint_dict:16,constraintdict:[0,16,20],constraints_dict:16,constraintz:20,construct:[9,20],consts_dict:16,contain:[0,1,2,7,8,9,10,11,14,16,17,19,20],contigu:7,control:[2,4,9,10,11,12,13,15,16,18,20],control_const:20,controller_cap:[11,16],controller_const:[],controller_constraint:20,controller_id:[],controller_nam:20,controllerconstraint:[1,10,20],convent:21,convert:20,core:7,core_num:7,correct:[17,21],correspond:[1,7,10,11,16,19,20],count:7,creat:[7,10,16,19,20],create_simulated_inst:7,cumul:[],current:[7,11,16],current_bottleneck_first:16,cx:1,data:[0,1,4,5,9,10,16,18,19,20],datafram:[7,19],defin:[0,16],degre:0,denot:[7,16],desir:20,destin:[4,10,11,12,13,15,16,20],detail:[4,17],determin:11,deviat:[7,13,20],df:7,dict:[7,10,11,16,20],dictionari:[2,7,10,11,16,18,20],differ:7,directli:7,directori:[7,20],discrep:7,displai:17,distinct:7,distribut:[12,13,15,20],divid:[0,16],doe:[16,21],done:7,dst_control:4,dure:[4,9],each:[7,12,13,15,16,19,20],earliest:16,element:[7,12,13,15],enough:16,ensur:21,entir:9,equal:[7,16],error:21,exactli:20,exceed:11,except:18,exclud:16,exclude_const:16,exist:16,existing_round:16,experi:[19,20],experiment:7,explicit:19,factor:[0,20],fals:[4,11,19],fewer:7,file:[7,9,10,15,19,20],file_dir:20,file_pattern:20,filenam:7,find:[7,16],find_scheduling_round:16,first:[7,12,13,15,16,20,21],first_lett:21,fit:[7,16],follow:[7,9,21],form:[1,4],format:19,formula:20,found:[9,17],from:[0,5,7,10,11,16,19,20],g:16,gaussian:[14,18],gaussiansimul:12,gener:[7,12,17,20],generate_controller_capac:20,generate_qos_capac:20,get:[7,20],get_all_files_by_pattern:20,get_bottleneck_constraint:16,get_bottleneck_migr:16,get_cap:[1,5],get_cap_dict:20,get_capac:0,get_constraint_dict:[],get_constraint_dict_for_control:20,get_constraint_dict_for_qos_group:20,get_constraints_dict:20,get_control:1,get_control_const:[],get_controller_cap_dict:20,get_controller_constraint:10,get_controller_constraint_dict:20,get_controller_id:10,get_controller_idx:1,get_cores_and_instances_per_cor:7,get_dst_control:4,get_group:[4,5],get_group_id:10,get_group_idx:5,get_heuristic_discrepancy_df:7,get_instances_for_cor:7,get_load:[0,4],get_load_factor:0,get_log_mean:20,get_log_std:20,get_migr:10,get_model_bound:9,get_model_data:9,get_proportion_bett:7,get_qos_const:[],get_qos_constraint:10,get_qos_constraint_dict:20,get_qos_group_cap_dict:20,get_qos_id:[],get_results_for_inst:7,get_results_head:20,get_round_id:[],get_round_reduction_stat:7,get_sim_tuples_for_cor:7,get_size_str:9,get_switch:[0,1,4,5],get_switch_id:10,get_switch_idx:4,get_time_df:7,get_total_load:[],given:[7,11,16,20],group:[4,5,7,9,10,11,12,13,15,16,20],group_col:7,group_nam:4,group_siz:20,gurobi:9,gurobipi:9,ha:[1,4,7,9,16,17],handl:[11,16,20],have:[7,16,19,20],header:20,help:7,heurist:[7,16,20],heuristic1:7,heuristic2:7,heuristic_col:7,high:[7,12,17,20,21],highest:16,hold:[0,7],id:[1,4,10],identifi:[0,4,7,20],ignor:16,ilp:7,implement:[16,19,21],impos:20,improv:7,includ:7,incorrect:17,incorrectbottleneckset:[17,21],incur:[0,4,12,13,15],index:[1,4,5,7,16,18,19],indic:[7,9,11,16,19,20],individu:12,info:0,inform:[0,1,4,5,11],initi:[7,9,17,20,21],initialize_and_join_process:7,initialize_se:20,input_dir:7,inspir:16,instanc:[2,7,8,9,10,12,13,14,15,16,17,18,20],instance_count:7,instance_data:[7,9,16,20],instance_fil:7,instance_idx:7,instance_s:7,instancedata:[7,9,10,16,20],instancenotspecifi:[9,17],instances_per_cor:7,instanti:9,integ:[1,4,5,7,9,10,11,12,13,15,16,20,21],interest:7,invalid:17,invalidnam:[1,4,17,21],involv:[4,10,16],is_in_group:4,iter:16,its:16,join:7,just:7,kei:[7,10,11,16,20],less:7,level:7,lh:0,line:[7,19],linear:9,list:[7,10,12,13,15,16,19,20],ln:20,load:[0,2,4,7,8,9,11,12,13,14,15,16,17,20],load_results_df:7,locat:7,loda:15,log:[14,18,20],log_scal:19,logarithm:19,lognorm:[13,20],lognormalsimul:13,loop:16,low:[12,17,20,21],lower:[9,19],machin:7,maintain:16,make:19,manag:7,match:20,max_cap:20,maximum:[5,7,11,12,13,15,16,20],mean:[13,20],medium:[12,17,20,21],member:4,messag:[9,17],method1:7,method2:7,method:[0,1,4,5,7,9,10,11,12,13,15],migrat:[0,1,5,7,8,9,10,12,13,14,15,16,17,20],migration_fil:[9,10],migrationschedul:[0,1,4,5,7,9,10,11,12,13,15,16,17,19,20,21],min_cap:20,minimum:20,mode:9,model:[7,9,10,11,17,18,20],modelnotoptim:17,modul:[2,7,8,14,16,17,18,19,20,21],most:16,mp:7,mu:[13,20],multiprocess:7,name:[0,1,4,5,7,10,11,15,16,17,19,20,21],need:1,none:[0,1,4,5,7,9,10,11,15,16,19,20,21],normal:[14,18,20],num_candid:16,num_choic:16,num_migr:15,num_round:16,number:[5,7,9,11,12,13,15,16,20],object:[1,7,9,10,11,12,13,15,16,17,20,21],object_typ:21,obtain:[7,16],one:[7,9,16,17,20,21],onli:9,opt_col:7,optim:[7,8,17,18,20],other:[7,16],otherwis:[4,7,9,11],outperform:7,output:[7,15,19],output_dir:7,output_fil:[7,15,19],over:7,overload:0,pack:16,page:18,panda:[7,19],paramet:[0,1,4,5,7,9,10,11,12,13,15,16,17,19,20,21],pars:[9,10],parse_migr:10,parser:[8,9,18],part:4,pass:7,path:9,pattern:20,pd:[7,19],per:[7,9,16],percent:7,percentag:7,perform:[4,7,19],pick:20,place:5,plot:18,plot_result:19,plot_result_v:[],plot_results_comparison:19,plot_runtim:19,possibl:16,pre:9,print:[9,11,19],print_migr:11,problem:[0,7,9,11,16],proc:7,process:7,program:9,proper:21,properli:21,proport:7,proposed_nam:21,qo:[2,4,9,10,11,12,13,15,16,18,20],qos_cap:[11,16],qos_const:20,qos_constraint:20,qos_id:[],qosconstraint:[5,10,20],qoscontraint:10,queri:17,rais:[0,1,4,9,17,21],random:20,rang:20,read:7,record:7,reduc:0,reduct:7,reflect:16,rel:[16,20],relat:[4,5,11,21],remain:[11,16],remov:[0,16],remove_migration_from_constraint:16,remove_switch:0,report:7,repres:[0,1,4,5,7,9,10,11,12,13,15,16,17,19,20,21],represent:[],reproduc:20,requir:7,respect:[],restrict:7,result:[7,19,20],result_col:19,results_col:19,results_df:[7,19],results_fil:7,results_list:7,retriev:[7,9,20],rh:0,roughli:7,round:[0,7,8,9,16,18,20],round_id:[],round_num:11,run:[7,15,16,20],run_optim:[7,20],runtim:19,s:[1,16,19],same:[7,16],sampl:[16,20],sample_with_log_op:20,scale:19,schedul:[0,7,8,9,11,12,13,14,15,17,20],schedule_migr:11,schedule_migration_in_earliest_round:16,sdn:4,search:[17,18,20],second:[7,12,13,15,20],seed:20,seed_num:20,select:16,select_bottleneck_migr:16,select_candidate_migr:16,select_migration_from_constraint:[],separ:[7,9,20],serv:15,set:[0,1,4,5,10,11,12,16,17,20,21],should:[4,16,19],sigma:[13,20],signal:[16,21],signifi:[4,16],sim:[12,13,15],sim_arg:7,sim_cl:7,sim_tupl:7,sims_per_cor:7,simul:[7,18],simulate_all_inst:7,simulate_inst:7,simultan:5,singl:[0,11,16,20],size:[7,9,20],so:7,solut:[7,9,20],solv:[7,9,16,20],sort:7,sort_col:7,sourc:[0,1,4,5,7,9,10,11,12,13,15,16,17,19,20,21],space:[7,9,20],specif:[15,20],specifi:[7,9,10,12,13,15,16,17,20],sqrt:20,standard:[13,19,20],start:7,start_idx:7,statist:7,store:[1,2,4,5,11,20],str:[0,1,4,5,7,9,10,12,15,16,17,19,20,21],string:[0,1,4,5,7,9,10,11,12,15,16,17,19,20,21],subset:[7,20],sum:[15,16,20],suppli:17,supplied_set:[17,21],switch_id:[],switch_load:0,switch_nam:[0,1,5,17],switchnotfound:[0,17],sx:4,system:7,take:[5,9],taken:[7,20],than:7,thi:[0,4,7,12,13,15,16,19,21],third:15,three:15,through:[16,20],time:7,time_col:7,time_var:19,titl:19,to_data:10,total:0,transit:[],tri:17,tupl:[7,12,13,15],two:[7,12,13,20],type:7,underli:[13,20],uninitializedmodel:17,updat:[10,16],upper:[9,19],upper_bound_round:[],us:[0,1,2,4,7,8,9,10,11,12,13,14,15,16,17,19,20,21],user:17,util:18,valid:[1,4,18],validate_bottleneck_set:21,validate_nam:21,valu:[1,7,9,10,11,12,16,19,20],variabl:[7,19],vector:[7,16],vector_first_fit:16,verbos:9,version:16,visual:19,we:16,were:0,when:[4,7,16,17,20],where:[1,4,7,20],whether:[7,9,11,19,20,21],which:[0,1,4,5,7,15,16,19,20,21],within:[5,20],without:11,work:8,would:0,write:7,write_results_to_fil:7,written:7,x:[1,4,7,19],x_titl:19,x_var:19,y:19,y_titl:19,yet:[9,17]},titles:["Constraint Dictionary","Controller Constraint","Migration Scheduling Data","Instance Data","Switch Migration","QoS Constraint","Migration Simulator","Analysis","Model","Optimizer","Parser","Migration Round","Gaussian Simulator","Log Normal Simulator","Simulation","Simulator","Scheduling Algorithms","Exceptions","Welcome to Load Migration Scheduling\u2019s documentation!","Plotting","Utility Functions","Validation"],titleterms:{"function":20,"switch":4,algorithm:16,analysi:7,constraint:[0,1,5],control:1,data:[2,3],dictionari:0,document:18,except:17,gaussian:12,indic:18,instanc:3,load:18,log:13,migrat:[2,4,6,11,18],model:8,normal:13,optim:9,parser:10,plot:19,qo:5,round:11,s:18,schedul:[2,16,18],simul:[6,12,13,14,15],tabl:18,util:20,valid:21,welcom:18}})