# Compiler settings and warnings for TCLEDTable project

# Create interface library for common compile options
if(NOT TARGET TCLEDTable_warnings)
    add_library(TCLEDTable_warnings INTERFACE)
endif()

# Set compile features
target_compile_features(TCLEDTable_warnings INTERFACE
    cxx_std_17
)

# Compiler-specific warnings and settings
if(MSVC)
    target_compile_options(TCLEDTable_warnings INTERFACE
        /W4                     # High warning level
        /permissive-           # Enforce standards compliance
        /w14640                # Enable warning on thread unsafe static member initialization
        /w14242                # 'identifier': conversion from 'type1' to 'type1', possible loss of data
        /w14254                # 'operator': conversion from 'type1:field_bits' to 'type1:field_bits', possible loss of data
        /w14263                # 'function': member function does not override any base class virtual member function
        /w14265                # 'classname': class has virtual functions, but destructor is not virtual
        /w14287                # 'operator': unsigned/negative constant mismatch
        /we4289                # nonstandard extension used: 'variable': loop control variable declared in the for-loop is used outside the for-loop scope
        /w14296                # 'operator': expression is always 'boolean_value'
        /w14311                # 'variable': pointer truncation from 'type1' to 'type2'
        /w14545                # expression before comma evaluates to a function which is missing an argument list
        /w14546                # function call before comma missing argument list
        /w14547                # 'operator': operator before comma has no effect; expected operator with side-effect
        /w14549                # 'operator': operator before comma has no effect; did you intend 'operator'?
        /w14555                # expression has no effect; expected expression with side-effect
        /w14619                # pragma warning: there is no warning number 'number'
        /w14640                # Enable warning on thread unsafe static member initialization
        /w14826                # Conversion from 'type1' to 'type_2' is sign-extended. This may cause unexpected runtime behavior.
        /w14905                # wide string literal cast to 'LPSTR'
        /w14906                # string literal cast to 'LPWSTR'
        /w14928                # illegal copy-initialization; more than one user-defined conversion has been implicitly applied
    )
    
    # Platform definitions for Windows
    target_compile_definitions(TCLEDTable_warnings INTERFACE
        WIN32_LEAN_AND_MEAN
        NOMINMAX
        _WIN64
        WIN64
    )
else()
    target_compile_options(TCLEDTable_warnings INTERFACE
        -Wall
        -Wextra
        -Wpedantic
        -Wshadow
        -Wnon-virtual-dtor
        -Wold-style-cast
        -Wcast-align
        -Wunused
        -Woverloaded-virtual
        -Wconversion
        -Wsign-conversion
        -Wnull-dereference
        -Wdouble-promotion
        -Wformat=2
        -Wimplicit-fallthrough
    )
    
    # Additional GCC-specific warnings
    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
        target_compile_options(TCLEDTable_warnings INTERFACE
            -Wmisleading-indentation
            -Wduplicated-cond
            -Wduplicated-branches
            -Wlogical-op
            -Wuseless-cast
        )
    endif()
    
    # Additional Clang-specific warnings
    if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        target_compile_options(TCLEDTable_warnings INTERFACE
            -Wlifetime
        )
    endif()
endif()

# Debug/Release specific settings
target_compile_definitions(TCLEDTable_warnings INTERFACE
    $<$<CONFIG:Debug>:DEBUG>
    $<$<CONFIG:Release>:NDEBUG>
)

# Position Independent Code for shared libraries
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
