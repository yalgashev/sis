-- SIS Database Schema Export
-- Generated on: 2025-10-23 15:42:17.298888
-- Database: sis

-- Table: academic_groups
CREATE TABLE public.academic_groups (id bigint NOT NULL, group_name character varying(100) NOT NULL, study_year integer NOT NULL, semester integer NOT NULL, academic_year character varying(20) NOT NULL, max_students integer NOT NULL, current_students integer NOT NULL, group_code character varying(20) , description text , is_active boolean NOT NULL, created_at timestamp with time zone NOT NULL, updated_at timestamp with time zone NOT NULL, department_id bigint NOT NULL, school_id bigint NOT NULL);

-- Table: admin
CREATE TABLE public.admin (id integer NOT NULL DEFAULT nextval('admin_id_seq'::regclass), first_name character varying(100) NOT NULL, last_name character varying(100) NOT NULL, username character varying(50) NOT NULL, password character varying(255) NOT NULL, email character varying(255) NOT NULL, phone_number character varying(20) , is_active boolean  DEFAULT true, is_super_admin boolean  DEFAULT false, last_login timestamp without time zone , created_at timestamp without time zone  DEFAULT CURRENT_TIMESTAMP, updated_at timestamp without time zone  DEFAULT CURRENT_TIMESTAMP);

-- Table: departments
CREATE TABLE public.departments (id bigint NOT NULL, name character varying(200) NOT NULL, code character varying(10) NOT NULL, head_name character varying(200) , phone character varying(20) , email character varying(254) , office_location character varying(100) , description text , is_active boolean NOT NULL, created_at timestamp with time zone NOT NULL, updated_at timestamp with time zone NOT NULL, school_id bigint NOT NULL);

-- Table: schools
CREATE TABLE public.schools (id bigint NOT NULL, name character varying(200) NOT NULL, code character varying(10) NOT NULL, address text , phone character varying(20) , email character varying(254) , website character varying(200) , established_date date , description text , is_active boolean NOT NULL, created_at timestamp with time zone NOT NULL, updated_at timestamp with time zone NOT NULL);

-- Table: students
CREATE TABLE public.students (id integer NOT NULL, first_name character varying(100) NOT NULL, last_name character varying(100) NOT NULL, middle_name character varying(100) , birthday date , nation character varying(50) NOT NULL, home_address text , phone_number character varying(20) , email character varying(254) , telegram_username character varying(100) , marital_status character varying(20) NOT NULL, is_from_large_family boolean NOT NULL, is_from_low_income_family boolean NOT NULL, is_from_troubled_family boolean NOT NULL, are_parents_deceased boolean NOT NULL, has_disability boolean NOT NULL, father_first_name character varying(100) , father_last_name character varying(100) , father_middle_name character varying(100) , father_phone_number character varying(20) , father_telegram_username character varying(100) , is_father_retired boolean NOT NULL, is_father_disabled boolean NOT NULL, mother_first_name character varying(100) , mother_last_name character varying(100) , mother_middle_name character varying(100) , mother_phone_number character varying(20) , mother_telegram_username character varying(100) , is_mother_retired boolean NOT NULL, is_mother_disabled boolean NOT NULL, photo character varying(100) , is_active boolean NOT NULL, created_at timestamp with time zone NOT NULL, updated_at timestamp with time zone NOT NULL, academic_group_id bigint NOT NULL, student_id character varying(20) , is_father_deceased boolean NOT NULL, is_mother_deceased boolean NOT NULL, id_card character varying(20) , last_login timestamp with time zone , password character varying(128) , username character varying(20) , children_count integer NOT NULL, guardian_name character varying(200) , guardian_phone_number character varying(20) , hobbies character varying(200) , languages_spoken character varying(200) , siblings_count integer NOT NULL, special_skills character varying(200) , gender character varying(10) , are_parents_divorced boolean NOT NULL);

-- Table: tutors
CREATE TABLE public.tutors (id bigint NOT NULL, first_name character varying(100) NOT NULL, last_name character varying(100) NOT NULL, username character varying(50) NOT NULL, password character varying(255) NOT NULL, email character varying(254) NOT NULL, phone_number character varying(20) , date_joined timestamp with time zone NOT NULL, last_login timestamp with time zone , is_active boolean NOT NULL, created_at timestamp with time zone NOT NULL, updated_at timestamp with time zone NOT NULL);

-- Table: tutors_assigned_groups
CREATE TABLE public.tutors_assigned_groups (id bigint NOT NULL, tutor_id bigint NOT NULL, academicgroup_id bigint NOT NULL);

