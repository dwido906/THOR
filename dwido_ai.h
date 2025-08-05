/*
 * DWIDO AI - Unified Artificial Intelligence System for ODIN OS
 * The world's first integrated OS-level AI assistant
 *
 * DWIDO: Dynamic Wisdom Intelligence with Distributed Operations
 * Modes: Gaming, Development, Research
 *
 * Copyright (c) 2025 North Bay Studios
 * Built for ODIN GAMER/DEV OS with FREYA kernel integration
 */

#ifndef DWIDO_AI_H
#define DWIDO_AI_H

#include <stdint.h>
#include <stdbool.h>
#include <pthread.h>
#include <time.h>

// DWIDO AI Version
#define DWIDO_VERSION_MAJOR 1
#define DWIDO_VERSION_MINOR 0
#define DWIDO_VERSION_PATCH 0
#define DWIDO_CODENAME "GENESIS"

// DWIDO Operation Modes
typedef enum
{
    DWIDO_MODE_INACTIVE = 0,
    DWIDO_MODE_GAMING = 1,
    DWIDO_MODE_DEVELOPMENT = 2,
    DWIDO_MODE_RESEARCH = 3,
    DWIDO_MODE_HYBRID = 4
} dwido_mode_t;

// DWIDO Priority Levels
typedef enum
{
    DWIDO_PRIORITY_LOW = 0,
    DWIDO_PRIORITY_NORMAL = 1,
    DWIDO_PRIORITY_HIGH = 2,
    DWIDO_PRIORITY_CRITICAL = 3,
    DWIDO_PRIORITY_REALTIME = 4
} dwido_priority_t;

// DWIDO Task Types
typedef enum
{
    DWIDO_TASK_ANALYSIS = 0,
    DWIDO_TASK_OPTIMIZATION = 1,
    DWIDO_TASK_GENERATION = 2,
    DWIDO_TASK_MONITORING = 3,
    DWIDO_TASK_LEARNING = 4,
    DWIDO_TASK_PREDICTION = 5
} dwido_task_type_t;

// Hardware Resource Types
typedef enum
{
    DWIDO_RESOURCE_CPU = 0,
    DWIDO_RESOURCE_GPU = 1,
    DWIDO_RESOURCE_MEMORY = 2,
    DWIDO_RESOURCE_STORAGE = 3,
    DWIDO_RESOURCE_NETWORK = 4
} dwido_resource_type_t;

// Neural Network Architecture
typedef struct
{
    uint32_t layers;
    uint32_t neurons_per_layer;
    uint32_t connections;
    float learning_rate;
    float dropout_rate;
    bool use_gpu_acceleration;
    char architecture_name[64];
} dwido_neural_config_t;

// Memory Pool for AI Operations
typedef struct
{
    void *base_address;
    size_t total_size;
    size_t used_size;
    size_t block_count;
    bool is_gpu_memory;
    pthread_mutex_t mutex;
} dwido_memory_pool_t;

// Hardware Resource Manager
typedef struct
{
    float cpu_usage_percent;
    float gpu_usage_percent;
    uint64_t memory_used_mb;
    uint64_t memory_available_mb;
    float gpu_memory_used_percent;
    uint32_t active_cuda_cores;
    float temperature_cpu;
    float temperature_gpu;
    bool hardware_acceleration_available;
    dwido_memory_pool_t cpu_pool;
    dwido_memory_pool_t gpu_pool;
} dwido_hardware_manager_t;

// DWIDO Task Structure
typedef struct dwido_task
{
    uint32_t task_id;
    dwido_task_type_t type;
    dwido_priority_t priority;
    dwido_mode_t required_mode;
    void *task_data;
    size_t data_size;
    uint64_t creation_time;
    uint64_t execution_time;
    bool is_completed;
    int (*execute_function)(struct dwido_task *task);
    struct dwido_task *next;
} dwido_task_t;

// Mode-Specific Configurations
typedef struct
{
    // Gaming Mode Configuration
    struct
    {
        bool performance_monitoring;
        bool real_time_optimization;
        bool competitive_analysis;
        bool fps_optimization;
        bool latency_reduction;
        float cpu_allocation_percent;
        float gpu_allocation_percent;
    } gaming;

    // Development Mode Configuration
    struct
    {
        bool code_generation;
        bool syntax_analysis;
        bool debugging_assistance;
        bool architecture_planning;
        bool pair_programming;
        uint32_t max_code_context_lines;
        bool auto_completion;
    } development;

    // Research Mode Configuration
    struct
    {
        bool neural_training;
        bool model_experimentation;
        bool data_analysis;
        bool algorithm_optimization;
        bool distributed_computing;
        uint32_t max_training_epochs;
        float learning_rate_adaptation;
    } research;
} dwido_mode_config_t;

// Knowledge Base Entry
typedef struct
{
    char category[64];
    char topic[128];
    char *content;
    size_t content_size;
    float relevance_score;
    uint64_t access_count;
    uint64_t last_updated;
    bool is_learned;
} dwido_knowledge_entry_t;

// User Interaction Context
typedef struct
{
    char current_application[256];
    char current_project[256];
    char working_directory[512];
    uint32_t session_duration_minutes;
    uint32_t commands_executed;
    dwido_mode_t preferred_mode;
    float user_skill_level;
    bool voice_interaction_enabled;
    bool learning_mode_enabled;
} dwido_user_context_t;

// Main DWIDO AI Core Structure
typedef struct
{
    // Core System
    uint32_t dwido_id;
    dwido_mode_t current_mode;
    dwido_mode_t previous_mode;
    bool is_active;
    bool is_learning;
    uint64_t boot_time;
    uint64_t total_operations;

    // Hardware Management
    dwido_hardware_manager_t hardware;

    // Mode Configuration
    dwido_mode_config_t mode_config;

    // Neural Networks (one per mode)
    dwido_neural_config_t gaming_neural;
    dwido_neural_config_t development_neural;
    dwido_neural_config_t research_neural;

    // Task Management
    dwido_task_t *task_queue_head;
    dwido_task_t *task_queue_tail;
    uint32_t active_tasks;
    uint32_t completed_tasks;
    pthread_mutex_t task_mutex;

    // Knowledge Base
    dwido_knowledge_entry_t *knowledge_base;
    uint32_t knowledge_entries;
    uint32_t max_knowledge_entries;
    pthread_rwlock_t knowledge_lock;

    // User Context
    dwido_user_context_t user_context;

    // Performance Metrics
    float average_response_time_ms;
    float accuracy_rate;
    uint64_t successful_predictions;
    uint64_t total_predictions;

    // Threading
    pthread_t main_thread;
    pthread_t mode_switch_thread;
    pthread_t learning_thread;
    pthread_t monitoring_thread;
    bool threads_active;

} dwido_ai_core_t;

// Global DWIDO instance
extern dwido_ai_core_t dwido_ai;

/*
 * DWIDO CORE FUNCTIONS
 */

// Initialization and Shutdown
int dwido_ai_initialize(void);
int dwido_ai_start(void);
int dwido_ai_shutdown(void);
void dwido_ai_reset(void);

// Mode Management
int dwido_switch_mode(dwido_mode_t new_mode);
dwido_mode_t dwido_get_current_mode(void);
int dwido_configure_mode(dwido_mode_t mode, void *config);
bool dwido_can_switch_mode(dwido_mode_t target_mode);

// Task Management
uint32_t dwido_submit_task(dwido_task_type_t type, dwido_priority_t priority,
                           void *data, size_t data_size);
int dwido_execute_task(uint32_t task_id);
void dwido_cancel_task(uint32_t task_id);
dwido_task_t *dwido_get_task_status(uint32_t task_id);

// Hardware Resource Management
int dwido_allocate_resources(dwido_resource_type_t type, float percentage);
void dwido_release_resources(dwido_resource_type_t type);
float dwido_get_resource_usage(dwido_resource_type_t type);
bool dwido_has_gpu_acceleration(void);

// Memory Management
void *dwido_malloc(size_t size, bool use_gpu);
void dwido_free(void *ptr);
void *dwido_realloc(void *ptr, size_t new_size);
size_t dwido_get_memory_usage(void);

/*
 * GAMING MODE FUNCTIONS
 */

// Performance Optimization
int dwido_gaming_optimize_performance(void);
float dwido_gaming_get_fps_prediction(void);
int dwido_gaming_reduce_latency(void);
void dwido_gaming_monitor_resources(void);

// Strategy Assistance
int dwido_gaming_analyze_gameplay(const char *game_data);
char *dwido_gaming_suggest_strategy(const char *game_state);
float dwido_gaming_calculate_win_probability(const char *current_state);

// Real-time Optimization
int dwido_gaming_optimize_graphics_settings(void);
int dwido_gaming_balance_cpu_gpu_load(void);
void dwido_gaming_adjust_priority(int process_id);

/*
 * DEVELOPMENT MODE FUNCTIONS
 */

// Code Generation and Analysis
char *dwido_dev_generate_code(const char *specification);
int dwido_dev_analyze_syntax(const char *source_code);
char *dwido_dev_suggest_refactoring(const char *code_block);
char *dwido_dev_generate_documentation(const char *code);

// Debugging Assistance
char *dwido_dev_analyze_error(const char *error_message, const char *context);
char *dwido_dev_suggest_fix(const char *bug_description);
int dwido_dev_trace_execution(const char *binary_path);

// Architecture Planning
char *dwido_dev_design_architecture(const char *requirements);
char *dwido_dev_suggest_patterns(const char *problem_description);
int dwido_dev_validate_design(const char *architecture_spec);

// Pair Programming
int dwido_dev_start_pair_session(void);
char *dwido_dev_suggest_next_step(const char *current_code);
void dwido_dev_provide_feedback(const char *code_snippet);

/*
 * RESEARCH MODE FUNCTIONS
 */

// Neural Network Training
int dwido_research_train_network(dwido_neural_config_t *config,
                                 void *training_data, size_t data_size);
float dwido_research_evaluate_model(void *model, void *test_data);
int dwido_research_optimize_hyperparameters(dwido_neural_config_t *config);

// AI Experimentation
int dwido_research_experiment_architecture(const char *architecture_desc);
float dwido_research_benchmark_performance(const char *algorithm_name);
char *dwido_research_suggest_improvements(const char *current_approach);

// Data Analysis
char *dwido_research_analyze_dataset(void *data, size_t size, const char *format);
float *dwido_research_extract_features(void *raw_data, uint32_t *feature_count);
char *dwido_research_generate_insights(float *features, uint32_t count);

/*
 * KNOWLEDGE BASE FUNCTIONS
 */

// Knowledge Management
int dwido_kb_add_entry(const char *category, const char *topic,
                       const char *content);
char *dwido_kb_search(const char *query);
int dwido_kb_update_entry(const char *category, const char *topic,
                          const char *new_content);
void dwido_kb_optimize_storage(void);

// Learning Functions
int dwido_learn_from_interaction(const char *input, const char *output,
                                 float success_rating);
void dwido_adapt_to_user_patterns(void);
int dwido_save_learned_knowledge(const char *filename);
int dwido_load_learned_knowledge(const char *filename);

/*
 * USER INTERACTION FUNCTIONS
 */

// Text Interface
char *dwido_process_text_input(const char *input);
int dwido_set_context(const char *application, const char *project);
char *dwido_get_suggestion(const char *current_task);

// Voice Interface
int dwido_initialize_voice_recognition(void);
char *dwido_process_voice_input(float *audio_data, size_t samples);
int dwido_synthesize_speech(const char *text, float *output_audio);

// Context Awareness
void dwido_update_user_context(void);
float dwido_assess_user_skill_level(void);
dwido_mode_t dwido_predict_needed_mode(void);

/*
 * INTEGRATION WITH ODIN/FREYA
 */

// ODIN OS Integration
int dwido_integrate_with_odin(void);
void dwido_register_odin_callbacks(void);
int dwido_access_odin_services(const char *service_name);

// FREYA Kernel Integration
int dwido_register_freya_neural_hooks(void);
void dwido_use_freya_compute_units(void);
int dwido_coordinate_with_freya_ai(void);

// System Monitoring
void dwido_monitor_system_performance(void);
int dwido_optimize_system_resources(void);
void dwido_report_to_odin_orchestrator(void);

/*
 * CUDA/GPU ACCELERATION
 */

// GPU Management
int dwido_initialize_cuda(void);
int dwido_allocate_gpu_memory(size_t size);
int dwido_execute_cuda_kernel(void *kernel_function, void *params);
void dwido_synchronize_gpu(void);

// Neural Network GPU Operations
int dwido_gpu_forward_pass(float *input, float *weights, float *output);
int dwido_gpu_backward_pass(float *gradients, float *weights);
int dwido_gpu_update_weights(float *weights, float *gradients, float learning_rate);

/*
 * UTILITY FUNCTIONS
 */

// Logging and Debugging
void dwido_log(int level, const char *format, ...);
void dwido_debug_dump_state(void);
char *dwido_get_status_report(void);

// Performance Monitoring
uint64_t dwido_get_execution_time_us(void);
float dwido_get_cpu_usage(void);
size_t dwido_get_memory_footprint(void);

// Configuration
int dwido_load_config(const char *config_file);
int dwido_save_config(const char *config_file);
void dwido_reset_to_defaults(void);

/*
 * MACROS FOR COMMON OPERATIONS
 */

#define DWIDO_GAMING_MODE() (dwido_ai.current_mode == DWIDO_MODE_GAMING)
#define DWIDO_DEV_MODE() (dwido_ai.current_mode == DWIDO_MODE_DEVELOPMENT)
#define DWIDO_RESEARCH_MODE() (dwido_ai.current_mode == DWIDO_MODE_RESEARCH)

#define DWIDO_SUBMIT_HIGH_PRIORITY_TASK(type, data, size) \
    dwido_submit_task(type, DWIDO_PRIORITY_HIGH, data, size)

#define DWIDO_QUICK_SWITCH(mode)         \
    do                                   \
    {                                    \
        if (dwido_can_switch_mode(mode)) \
        {                                \
            dwido_switch_mode(mode);     \
        }                                \
    } while (0)

#define DWIDO_LOG_INFO(msg, ...) dwido_log(1, msg, ##__VA_ARGS__)
#define DWIDO_LOG_ERROR(msg, ...) dwido_log(3, msg, ##__VA_ARGS__)

#endif // DWIDO_AI_H
