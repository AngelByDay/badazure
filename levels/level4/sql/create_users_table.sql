SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[users](
	[UserId] [uniqueidentifier] NOT NULL,
	[Username] [varchar](64) NOT NULL,
	[Passwd] [varchar](128) NOT NULL,
	[DisplayName] [varchar](128) NULL,
	[Email] [varchar](256) NULL,
	[Dept] [varchar](32) NULL,
	[Active] [int] NULL,
	[Locked] [int] NULL,
	[CreatedDate] [datetime] NULL,
	[ModifiedDate] [datetime] NULL,
	[ModifiedUser] [datetime] NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[users] ADD PRIMARY KEY CLUSTERED 
(
	[UserId] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[users] ADD  DEFAULT (newid()) FOR [UserId]
GO