USE [master]
GO
CREATE DATABASE [Medsurance]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'Medsurance', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\Medsurance.mdf' , SIZE = 1317888KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'Medsurance_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\Medsurance_log.ldf' , SIZE = 653120KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [Medsurance] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [Medsurance].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [Medsurance] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [Medsurance] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [Medsurance] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [Medsurance] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [Medsurance] SET ARITHABORT OFF 
GO
ALTER DATABASE [Medsurance] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [Medsurance] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [Medsurance] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [Medsurance] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [Medsurance] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [Medsurance] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [Medsurance] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [Medsurance] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [Medsurance] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [Medsurance] SET  DISABLE_BROKER 
GO
ALTER DATABASE [Medsurance] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [Medsurance] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [Medsurance] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [Medsurance] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [Medsurance] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [Medsurance] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [Medsurance] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [Medsurance] SET RECOVERY FULL 
GO
ALTER DATABASE [Medsurance] SET  MULTI_USER 
GO
ALTER DATABASE [Medsurance] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [Medsurance] SET DB_CHAINING OFF 
GO
ALTER DATABASE [Medsurance] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [Medsurance] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [Medsurance] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [Medsurance] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [Medsurance] SET QUERY_STORE = OFF
GO
USE [Medsurance]
GO
/****** Object:  Table [dbo].[Locations]    Script Date: 29/05/2025 16:46:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Locations](
	[county_code] [bigint] NOT NULL,
	[county_name] [varchar](50) NULL,
	[state_code] [varchar](8) NULL,
	[rating_area] [varchar](50) NULL,
 CONSTRAINT [PK_Locations_county_code] PRIMARY KEY CLUSTERED 
(
	[county_code] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PlanCSR]    Script Date: 29/05/2025 16:46:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PlanCSR](
	[plan_id] [varchar](50) NULL,
	[csr_variant] [varchar](50) NULL,
	[service_type] [varchar](50) NULL,
	[cost_type] [varchar](50) NULL,
	[value] [bigint] NULL,
	[unit] [varchar](50) NULL,
	[applies_after_deductible] [bit] NULL,
	[unit_time] [varchar](50) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PlanPremiums]    Script Date: 29/05/2025 16:46:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PlanPremiums](
	[plan_id] [varchar](50) NULL,
	[age_group] [int] NULL,
	[family_type] [varchar](50) NULL,
	[premium] [decimal](18, 0) NULL,
	[ehb_percent] [decimal](6, 0) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Plans]    Script Date: 29/05/2025 16:46:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Plans](
	[plan_id] [varchar](50) NOT NULL,
	[county_code] [bigint] NOT NULL,
	[plan_name] [varchar](250) NULL,
	[issuer_name] [varchar](250) NULL,
	[meta_level] [varchar](50) NULL,
	[plan_type] [varchar](50) NULL,
	[customer_service_phone_number] [varchar](50) NULL,
	[benifits_summary_url] [varchar](150) NULL,
	[adult_dental] [bit] NULL,
	[child_dental] [bit] NULL,
 CONSTRAINT [PK_Plans_plan_id] PRIMARY KEY CLUSTERED 
(
	[plan_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[PlanCSR]  WITH CHECK ADD  CONSTRAINT [FK_PlanCSR_plan_id] FOREIGN KEY([plan_id])
REFERENCES [dbo].[Plans] ([plan_id])
GO
ALTER TABLE [dbo].[PlanCSR] CHECK CONSTRAINT [FK_PlanCSR_plan_id]
GO
ALTER TABLE [dbo].[PlanPremiums]  WITH CHECK ADD  CONSTRAINT [FK_PlanPremiums_plan_id] FOREIGN KEY([plan_id])
REFERENCES [dbo].[Plans] ([plan_id])
GO
ALTER TABLE [dbo].[PlanPremiums] CHECK CONSTRAINT [FK_PlanPremiums_plan_id]
GO
ALTER TABLE [dbo].[Plans]  WITH CHECK ADD  CONSTRAINT [FK_Plans_County_code] FOREIGN KEY([county_code])
REFERENCES [dbo].[Locations] ([county_code])
GO
ALTER TABLE [dbo].[Plans] CHECK CONSTRAINT [FK_Plans_County_code]
GO
USE [master]
GO
ALTER DATABASE [Medsurance] SET  READ_WRITE 
GO
